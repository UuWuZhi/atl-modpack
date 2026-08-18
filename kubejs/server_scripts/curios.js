let $Player = Java.loadClass("net.minecraft.world.entity.player.Player")
const curiosHelper = Java.loadClass("top.theillusivec4.curios.api.CuriosApi").getCuriosHelper()
 
function isEquippedCurio(entity, curioId) {
    return curiosHelper.findFirstCurio(entity, curioId).isPresent()
}
 
ServerEvents.tags("item", event => {
    event.add("curios:belt", "kubejs:flying_soul")
})
 
PlayerEvents.tick(event => {
    let player = event.player
    if ( isEquippedCurio(player, "kubejs:flying_soul") ) {
                    player.abilities.mayfly = true
                    player.onUpdateAbilities()
    }
})

PlayerEvents.tick(event => {
    let player = event.player
    if ( !isEquippedCurio(player, "kubejs:flying_soul") ) {
                    if (player.isCreative()) return
                    player.abilities.mayfly = false
                    player.abilities.flying = false
                    player.onUpdateAbilities()
    }
})