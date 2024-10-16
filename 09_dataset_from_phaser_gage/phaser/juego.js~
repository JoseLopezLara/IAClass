var fondo;
var w=800, h=400; 
var jugador;
var game = new Phaser.Game(w, h, Phaser.AUTO, '',{preload: preload, create:create, update:update} );

function preload(){
    game.load.image('fondo', 'assets/game/fondo.jpg' );
    game.load.spritesheet('mono', 'assets/sprites/player.png',32,48);
}

function create() {
    game.physics.startSystem(Phaser.Physics.ARCADE);
    game.physics.arcade.gravity.y=800;
    game.time.desiredFps=30;
    
    fondo = game.add.tileSprite(0,0,w,h,'fondo');
    jugador = game.add.sprite(50, h, 'mono');



    game.physics.enable(jugador);
    jugador.body.collideWorldBounds = true;
    var run = jugador.animations.add('run');
    jugador.animations.play('run', 10, true);

    pause_label = game.add.text(w - 100, 20, 'Pause', { font: '20px Arial', fill: '#fff' });
    pause_label.inputEnabled = true;
    //pause_label.events.onInputUp.add(pause, self);
    //game.input.onDown.add(un_pause, self);

    
    jumpButton = game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);

}

function jump(){
    jugador.body.velocity.y = -78;
    
}

function update(){
    game.physics.arcade.collide(jugador, null, this);
    fondo.tilePosition.x -= 1;

    if( jumpButton.isDown){
        jump();
    }

}
