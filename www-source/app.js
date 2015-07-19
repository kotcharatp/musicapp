var target = document.getElementById('point');

// create the timeline
tl = new TimelineMax();

// get the screen size
var screen_height = window.innerHeight;
var screen_width = window.innerWidth;

// find maximum and minimum frequency
var max = 0;
var min = 1000000;
for( var i = 0; i < dataset.length; i++ ) {
    var o = dataset[i];
    if( o.f > max ) max = o.f;
    if( o.f < min ) min = o.f;
}

// calculate step size
step_size = screen_height / ( max-min );


// create svg drawing
   var draw = SVG('drawing')

   // create text
   var text = draw.text('SVG.JS').move(300, 0)
   text.font({
     color: white,
     family: 'Source Sans Pro'
   , size: 180
   , anchor: 'middle'
   , leading: 1
   })
