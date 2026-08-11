Ponder.registry((event) => {
        event.create("tofucraft:blocksaltpan").scene("blocksaltpan", "晒盐", "kubejs:ponder", (scene, util) => {
            scene.world.setBlocks([4,1,4], "tofucraft:blocksaltpan")
            scene.showBasePlate()
            scene.idle(20)
            scene.world.showSection([0,1,0,8,8,8], Direction.down)
            scene.scaleSceneView(1)
            scene.idle(20);
            scene
                .text(60, "你可以使用盐田来晒盐，并获得盐卤等材料", [4,1.5,4])
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene.world.modifyBlock([4,1,4], (state) => state.with("stat", "water"), false)
            scene
                .text(60, "只需要倒入水，然后等待...", [4,1.5,4])
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene.world.modifyBlock([4,1,4], (state) => state.with("stat", "salt"), false)
            scene
                .text(60, "一段时间后，盐田内的水会变为盐", [4,1.5,4])
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene
                .showControls(60, [4,2,4], "down")
                .rightClick()
            scene.world.modifyBlock([4,1,4], (state) => state.with("stat", "bittern"), false)
            scene
                .text(60, "用空手右键盐分，就可以获得盐", [4,1.5,4])
                .colored(PonderPalette.BLUE)
                .placeNearTarget()
                .attachKeyFrame();
            scene.idle(80);
            scene.world.modifyBlock([4,1,4], (state) => state.with("stat", "empty"), false)
            scene
                .text(60, "剩下的蓝色液体就是盐卤，\n使用空瓶右键，就可以获得盐卤", [4,1.5,4])
                .colored(PonderPalette.BLUE)
                .attachKeyFrame();
            scene
                .showControls(60, [4,2,4], "down")
                .rightClick()
                .withItem("glass_bottle")
            scene.idle(80);
        });
    });
    