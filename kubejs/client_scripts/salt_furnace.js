Ponder.registry((event) => {
        event.create("tofucraft:salt_furnace")
        .scene("salt_furnace_2", "自动化制盐", "kubejs:salt_furnace", (scene, util) => {
            scene.showBasePlate()
            scene.rotateCameraY(90)
            scene.idle(20)
            scene.world.showSection([0,1,0,8,8,8], Direction.down)
            scene
                .text(60, "你可以用管道或漏斗向盐炉中自动输入燃料、玻璃瓶和水")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .text(60, "盐只能通过下方输出")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .text(60, "盐卤需要输入玻璃瓶才能输出，\n但盐卤生产满后也不会影响盐的继续生产")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
        });
    });
    