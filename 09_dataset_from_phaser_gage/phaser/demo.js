var w=800, h=400;
var jugador;
var fondo;
var teclas;

var juego = new Phaser.Game(w,h, Phaser.AUTO, '', {preload:preload, create:create, update:update});

function preload(){
    juego.load.image('fondo', 'assets/game/fondo.jpg');
    juego.load.spritesheet('mono', 'assets/sprites/player.png', 32,48);
    
}

function create(){

    fondo = juego.add.tileSprite(0,0,w,h,'fondo');
    jugador = juego.add.sprite(200,30, 'mono');


    /*  juego.physics.startSystem(Phaser.Physics.ARCADE);
    juego.physics.arcade.gravity.y = 400;
    juego.time.desiredFps = 30;


    fondo = juego.add.tileSprite(0,0,w,h,'fondo');
    jugador = juego.add.sprite(200,30, 'mono');

    
    jugador.animations.add('right',[8,9,10,11]);
    jugador.animations.add('left',[4,5,6,7]);
    jugador.animations.add('up',[12,13,14,15]);
    jugador.animations.add('down',[0,1,2,3]);
    
    teclas = juego.input.keyboard.createCursorKeys();
    //juego.physics.arcade.enable(jugador);
    //jugador.body.collideWorldBounds=true;


    jumpButton = juego.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);
*/
}

function update(){


    //fondo.tilePosition.x -= 1; //moving background

    //juego.physics.arcade.collide( jugador, this);

/*    
    if(jumpButton.isDown){
	jugador.body.velocity.y=-232;
    }


    if (teclas.up.isDown)
    {
	jugador.animations.play('up', 10, true);
	jugador.y--;
    }
    else if (teclas.down.isDown)
    {
	jugador.animations.play('down', 10, true);
	jugador.y++;
    }

    if (teclas.left.isDown)
    {
        jugador.x--;
	jugador.animations.play('left', 10, true);
	//fondo.tilePosition.x -=1;
    }
    else if (teclas.right.isDown)
    {
        jugador.x++;
	jugador.animations.play('right', 10, true);

	//fondo.tilePosition.x -=1;

    }

*/    
}
