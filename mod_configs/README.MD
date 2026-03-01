# Mod Configurations
This is a list of config changes we will make to the mods. We will store these as a list in this MD file for now,
as storing the raw configs this early might cause issues.



## Create 
* All of the TEAW 4 changes like schematicannon speed and frotport range.
* Make a mod that uses a mixin mod to disable contraptions from assembling with auto-cannon parts.
    <details>
    <summary>Something like:</summary>

    ```java
    @Mixin(Contraption.class)
    public class ContraptionMixin {
        @Inject(method = "assemble", at = @At("TAIL"), cancellable = true)
        private void limitBadBlocks(Level level, BlockPos pos, CallbackInfoReturnable<Boolean> cir) {
            Contraption contraption = (Contraption)(Object)this;
            int autoCannons = 0;
            for (StructureBlockInfo info : contraption.getBlocks().values()) {
                if (info.state().getBlock() instanceof AutoCannonBlock) {
                    autoCannons++;

                    if (autoCannons > 256) {
                        cir.setReturnValue(false);
                        // Notify player somehow. Can we use Goggle tooltip?
                        return;
                    }
                }
            }
        }
    }
    ```
    </details>



## Storage Drawers
* Disable shulker functionality. Its overpowered to mail someone millions of items. 
`DropMode` should be set to `DROP`, with a stack limit of 32. This makes it
so items are not unfairly voided, so you can at least reclaim some items when breaking the drawer.
