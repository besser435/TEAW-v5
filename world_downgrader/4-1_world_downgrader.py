
import gzip
import io
import math
import os
import re
import struct
import zlib
from pathlib import Path

import nbtlib


SECTOR_SIZE = 4096
HEADER_SIZE = SECTOR_SIZE * 2

# Only these chunk compression types can be modified.
# Unsupported compression types are preserved without modification.
COMPRESSION_GZIP = 1
COMPRESSION_ZLIB = 2
COMPRESSION_NONE = 3

BLOCK_REPLACEMENTS = {
    # Pale Oak woodset
    "minecraft:pale_oak_log": "minecraft:dark_oak_log",
    "minecraft:stripped_pale_oak_log": "minecraft:stripped_birch_log",
    "minecraft:pale_oak_wood": "minecraft:birch_wood",
    "minecraft:stripped_pale_oak_wood": "minecraft:stripped_birch_wood",

    "minecraft:pale_oak_leaves": "minecraft:dark_oak_leaves",
    "minecraft:pale_oak_sapling": "minecraft:dark_oak_sapling",

    "minecraft:pale_oak_planks": "minecraft:birch_planks",
    "minecraft:pale_oak_slab": "minecraft:birch_slab",
    "minecraft:pale_oak_stairs": "minecraft:birch_stairs",
    "minecraft:pale_oak_fence": "minecraft:birch_fence",
    "minecraft:pale_oak_fence_gate": "minecraft:birch_fence_gate",
    "minecraft:pale_oak_door": "minecraft:birch_door",
    "minecraft:pale_oak_trapdoor": "minecraft:birch_trapdoor",
    "minecraft:pale_oak_pressure_plate": "minecraft:birch_pressure_plate",
    "minecraft:pale_oak_button": "minecraft:birch_button",
    "minecraft:pale_oak_sign": "minecraft:birch_sign",
    "minecraft:pale_oak_wall_sign": "minecraft:birch_wall_sign",
    "minecraft:pale_oak_hanging_sign": "minecraft:birch_hanging_sign",
    "minecraft:pale_oak_wall_hanging_sign": "minecraft:birch_wall_hanging_sign",

    # Pale Garden vegetation
    "minecraft:pale_moss_block": "minecraft:moss_block",
    "minecraft:pale_moss_carpet": "minecraft:moss_carpet",
    "minecraft:pale_hanging_moss": "minecraft:cave_vines_plant",  # plant so they dont grow or produce berries

    # Eyeblossoms
    "minecraft:closed_eyeblossom": "minecraft:oxeye_daisy",
    "minecraft:open_eyeblossom": "minecraft:orange_tulip",

    # Resin
    "minecraft:resin_clump": "minecraft:glow_lichen",
    "minecraft:resin_block": "minecraft:orange_terracotta",
    "minecraft:resin_bricks": "minecraft:bricks",
    "minecraft:resin_brick_stairs": "minecraft:brick_stairs",
    "minecraft:resin_brick_slab": "minecraft:brick_slab",
    "minecraft:resin_brick_wall": "minecraft:brick_wall",
    "minecraft:chiseled_resin_bricks": "minecraft:chiseled_stone_bricks",

    # Creaking Heart
    "minecraft:creaking_heart": "minecraft:dark_oak_log",

    # Dry grass
    #(this somehow got in there despite being a "1.21.4" world, maybe its just a registry or mod thing and it isnt actually there but putting it here in case)
    "minecraft:short_dry_grass": "minecraft:dead_bush",
    "minecraft:tall_dry_grass": "minecraft:dead_bush",
}

BIOME_REPLACEMENTS = {
    "minecraft:pale_garden": "minecraft:dark_forest",
}

# These replacement blocks have different block-state properties
# from their original blocks. Their old properties must be removed.
STRIP_PROPERTIES = {
    "minecraft:pale_hanging_moss",
    "minecraft:closed_eyeblossom",
    "minecraft:open_eyeblossom",
}

LOG_FILE_NAME = "downgrade_changes.log"


def decompress_chunk(payload, compression):
    if compression == COMPRESSION_GZIP:
        return gzip.decompress(payload)

    if compression == COMPRESSION_ZLIB:
        return zlib.decompress(payload)

    if compression == COMPRESSION_NONE:
        return payload

    raise ValueError(
        f"Unsupported chunk compression type: {compression}"
    )


def compress_chunk(data, compression):
    if compression == COMPRESSION_GZIP:
        return gzip.compress(data, mtime=0)

    if compression == COMPRESSION_ZLIB:
        return zlib.compress(data)

    if compression == COMPRESSION_NONE:
        return data

    raise ValueError(
        f"Unsupported chunk compression type: {compression}"
    )


def transform_chunk(nbt):
    """
    Modify block and biome palettes.

    Returns:
        (modified, block_counts, biome_counts)
    """

    modified = False
    block_counts = {}
    biome_counts = {}

    sections = nbt.get("sections", [])

    for section in sections:

        # -----------------------------------------
        # Block palettes
        # -----------------------------------------

        block_states = section.get("block_states")

        if block_states is not None:
            palette = block_states.get("palette", [])

            for block in palette:
                old_name = str(block.get("Name", ""))

                if old_name not in BLOCK_REPLACEMENTS:
                    continue

                new_name = BLOCK_REPLACEMENTS[old_name]

                # Creaking Hearts have additional properties
                # that Dark Oak Logs do not support.
                if old_name == "minecraft:creaking_heart":
                    properties = block.get("Properties")

                    if properties is not None:
                        axis = properties.get("axis")

                        if axis is not None:
                            block["Properties"] = nbtlib.Compound({
                                "axis": axis
                            })
                        else:
                            del block["Properties"]

                # These replacements have incompatible
                # properties, so use the replacement's defaults.
                elif old_name in STRIP_PROPERTIES:
                    if "Properties" in block:
                        del block["Properties"]

                block["Name"] = nbtlib.String(new_name)

                block_counts[old_name] = (
                    block_counts.get(old_name, 0) + 1
                )

                modified = True

        # -----------------------------------------
        # Biome palettes
        # -----------------------------------------

        biomes = section.get("biomes")

        if biomes is not None:
            palette = biomes.get("palette", [])

            for index, biome in enumerate(palette):
                old_name = str(biome)

                if old_name not in BIOME_REPLACEMENTS:
                    continue

                new_name = BIOME_REPLACEMENTS[old_name]

                palette[index] = nbtlib.String(new_name)

                biome_counts[old_name] = (
                    biome_counts.get(old_name, 0) + 1
                )

                modified = True

    return modified, block_counts, biome_counts


def read_region_chunks(region_path, region_x, region_z):
    """
    Read all occupied chunks from an Anvil region file.

    External chunks (.mcc) are supported and their payloads
    are read from the corresponding external files.
    """

    region_bytes = region_path.read_bytes()

    if len(region_bytes) < HEADER_SIZE:
        raise ValueError("Invalid region file: header is incomplete")

    if len(region_bytes) % SECTOR_SIZE != 0:
        raise ValueError("Invalid region file: file is not sector aligned")

    chunks = {}

    for index in range(1024):
        location = struct.unpack_from(
            ">I", region_bytes, index * 4
        )[0]

        if location == 0:
            continue

        sector_offset = location >> 8
        sector_count = location & 0xFF

        if sector_offset < 2 or sector_count == 0:
            raise ValueError(
                f"Invalid location entry in chunk slot {index}"
            )

        offset = sector_offset * SECTOR_SIZE

        if offset + 5 > len(region_bytes):
            raise ValueError(
                f"Chunk slot {index} points outside the region file"
            )

        length = struct.unpack_from(">I", region_bytes, offset)[0]

        if length < 1 or offset + 4 + length > len(region_bytes):
            raise ValueError(
                f"Invalid chunk length in slot {index}"
            )

        compression_byte = region_bytes[offset + 4]

        external = bool(compression_byte & 0x80)
        compression = compression_byte & 0x7F

        local_x = index % 32
        local_z = index // 32

        chunk_x = region_x * 32 + local_x
        chunk_z = region_z * 32 + local_z

        mcc_path = region_path.parent / (
            f"c.{chunk_x}.{chunk_z}.mcc"
        )

        if external:
            if not mcc_path.exists():
                raise FileNotFoundError(
                    f"External chunk file missing: {mcc_path}"
                )

            payload = mcc_path.read_bytes()

        else:
            payload = region_bytes[
                offset + 5: offset + 4 + length
            ]

        timestamp = struct.unpack_from(
            ">I", region_bytes, 4096 + index * 4
        )[0]

        chunks[index] = {
            "payload": payload,
            "compression": compression,
            "external": external,
            "timestamp": timestamp,
            "modified": False,
            "mcc_path": mcc_path,
        }

    return chunks


def rebuild_region(region_path, chunks):
    """
    Rebuild a complete region file with updated chunks.

    Existing chunk timestamps are preserved.
    Oversized chunks are stored as external .mcc files.
    """

    region_x, region_z = map(
        int,
        re.match(r"r\.(-?\d+)\.(-?\d+)\.mca$", region_path.name).groups()
    )

    output = bytearray(HEADER_SIZE)
    cursor_sector = 2

    external_files = set()
    obsolete_external_files = []

    for index in range(1024):
        chunk = chunks.get(index)

        if chunk is None:
            continue

        payload = chunk["payload"]
        compression = chunk["compression"]

        local_x = index % 32
        local_z = index // 32

        chunk_x = region_x * 32 + local_x
        chunk_z = region_z * 32 + local_z

        mcc_path = region_path.parent / (
            f"c.{chunk_x}.{chunk_z}.mcc"
        )

        length = len(payload) + 1

        record = (
            struct.pack(">I", length)
            + bytes([compression])
            + payload
        )

        sector_count = math.ceil(len(record) / SECTOR_SIZE)

        if sector_count <= 255:
            # Normal inline chunk
            struct.pack_into(
                ">I",
                output,
                index * 4,
                (cursor_sector << 8) | sector_count
            )

            output.extend(
                record.ljust(sector_count * SECTOR_SIZE, b"\x00")
            )

            if mcc_path.exists():
                obsolete_external_files.append(mcc_path)

        else:
            # External chunk storage
            external_files.add(mcc_path)

            temp_mcc = mcc_path.with_name(
                mcc_path.name + ".tmp"
            )

            temp_mcc.write_bytes(payload)
            os.replace(temp_mcc, mcc_path)

            external_record = (
                struct.pack(">I", 1)
                + bytes([compression | 0x80])
            )

            struct.pack_into(
                ">I",
                output,
                index * 4,
                (cursor_sector << 8) | 1
            )

            output.extend(
                external_record.ljust(SECTOR_SIZE, b"\x00")
            )

            sector_count = 1

        # Preserve original chunk timestamp
        struct.pack_into(
            ">I",
            output,
            4096 + index * 4,
            chunk["timestamp"]
        )

        cursor_sector += sector_count

    temp_region = region_path.with_name(
        region_path.name + ".tmp"
    )

    with open(temp_region, "wb") as file:
        file.write(output)
        file.flush()
        os.fsync(file.fileno())

    os.replace(temp_region, region_path)

    # Remove obsolete external files only after region save.
    for path in obsolete_external_files:
        if path not in external_files and path.exists():
            path.unlink()


def process_region(region_path, log_file):
    match = re.match(
        r"r\.(-?\d+)\.(-?\d+)\.mca$",
        region_path.name
    )

    if not match:
        return False

    region_x, region_z = map(int, match.groups())

    print(f"\n[Region] {region_path.name}")

    chunks = read_region_chunks(
        region_path,
        region_x,
        region_z
    )

    region_modified = False

    total_blocks = {}
    total_biomes = {}

    for index, chunk in chunks.items():

        compression = chunk["compression"]

        if compression not in (
            COMPRESSION_GZIP,
            COMPRESSION_ZLIB,
            COMPRESSION_NONE
        ):
            warning = (
                f"[Warning] {region_path.name}, chunk slot {index}: "
                f"unsupported compression {compression}"
            )

            print(warning)

            with open(log_file, "a", encoding="utf-8") as log:
                log.write(warning + "\n")

            continue

        try:
            raw_nbt = decompress_chunk(
                chunk["payload"],
                compression
            )

            nbt = nbtlib.File.parse(io.BytesIO(raw_nbt))

            modified, block_counts, biome_counts = (
                transform_chunk(nbt)
            )

            if not modified:
                continue

            output_buffer = io.BytesIO()
            nbt.write(output_buffer)

            new_payload = compress_chunk(
                output_buffer.getvalue(),
                compression
            )

            chunk["payload"] = new_payload
            chunk["modified"] = True

            region_modified = True

            for name, count in block_counts.items():
                total_blocks[name] = (
                    total_blocks.get(name, 0) + count
                )

            for name, count in biome_counts.items():
                total_biomes[name] = (
                    total_biomes.get(name, 0) + count
                )

        except Exception as error:
            print(
                f"[Warning] Could not process chunk slot "
                f"{index}: {error}"
            )

    if region_modified:
        rebuild_region(region_path, chunks)

        print("[Saved] Region updated.")

        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"\nRegion: {region_path.name}\n")

            for name, count in sorted(total_blocks.items()):
                log.write(
                    f"  BLOCK {name}: {count} palette entries\n"
                )

            for name, count in sorted(total_biomes.items()):
                log.write(
                    f"  BIOME {name}: {count} palette entries\n"
                )

    else:
        print("[Unchanged] No replacements found.")

    return region_modified


def downgrade_world(world_path):
    world_path = Path(world_path).expanduser().resolve()

    region_dir = world_path / "region"
    log_file = world_path / LOG_FILE_NAME

    if not world_path.is_dir():
        print("[Error] World directory does not exist.")
        return

    if not region_dir.is_dir():
        print("[Error] No Overworld region directory found.")
        return

    region_files = sorted(region_dir.glob("r.*.*.mca"))

    print("=" * 60)
    print("Minecraft 1.21.4 -> 1.21.1 World Conversion")
    print("=" * 60)
    print(f"World: {world_path}")
    print(f"Region files: {len(region_files)}")
    print("Dimension: Overworld only")
    print("=" * 60)

    log_file.write_text(
        "Minecraft world downgrade log\n",
        encoding="utf-8"
    )

    modified_regions = 0
    failed_regions = 0

    for index, region_path in enumerate(region_files, start=1):

        print(
            f"\n[Progress] Region {index}/{len(region_files)}"
        )

        try:
            if process_region(region_path, log_file):
                modified_regions += 1

        except Exception as error:
            failed_regions += 1

            print(
                f"[ERROR] Failed region {region_path.name}: {error}"
            )

            with open(log_file, "a", encoding="utf-8") as log:
                log.write(
                    f"\nERROR {region_path.name}: {error}\n"
                )

    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE - Check log to see if any regions failed to convert.")
    print("Be sure to delete the 'entities' directory if it exists, as it may contain entities with old data versions.")
    print("=" * 60)
    print(f"Regions scanned: {len(region_files)}")
    print(f"Regions modified: {modified_regions}")
    print(f"Failed regions: {failed_regions}")
    print(f"Log file: {log_file}")
    print("=" * 60)


if __name__ == "__main__":
    world_directory = input(
        "Enter the full path to your Minecraft world folder: "
    ).strip().strip('"')

    downgrade_world(world_directory)
