Ponder.registry((event) => {
        event.create("farmersdelight:stove")
        .scene("stove_1", "通用炉灶", "kubejs:stove", (scene, util) => {
            scene.showBasePlate()
            scene.rotateCameraY(90)
            scene.idle(20)
            scene.world.showSection([0,1,0,8,8,8], Direction.down)
            scene
                .text(60, "本整合包包含农夫乐事与森罗物语的两种炉灶")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .text(60, "当然，这两种炉灶是互通使用的")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .text(60, "你可以用森罗物语的炉灶去加热农夫乐事的厨具，\n反过来也一样可以")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
        });
        event.create("kaleidoscope_cookery:stove")
        .scene("stove_1", "通用炉灶", "kubejs:stove", (scene, util) => {
            scene.showBasePlate()
            scene.rotateCameraY(90)
            scene.idle(20)
            scene.world.showSection([0,1,0,8,8,8], Direction.down)
            scene
                .text(60, "本整合包包含农夫乐事与森罗物语的两种炉灶")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .text(60, "当然，这两种炉灶是互通使用的")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .text(60, "你可以用森罗物语的炉灶去加热农夫乐事的厨具，\n反过来也一样可以")
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
        });
    });
    