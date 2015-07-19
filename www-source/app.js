// locate target for animating
var p1 = document.getElementById('p1');
var p2 = document.getElementById('p2');
var p3 = document.getElementById('p3');
var p4 = document.getElementById('p4');
var p5 = document.getElementById('p5');

// create timelines
tl1 = new TimelineMax({ paused:true });
tl2 = new TimelineMax({ paused:true });
tl3 = new TimelineMax({ paused:true });
tl4 = new TimelineMax({ paused:true });
tl5 = new TimelineMax({ paused:true });

// define margins for our objects
bottom_margin = 50;
top_margin = 10;

// get the screen size
var screen_height = window.innerHeight - bottom_margin - top_margin;        // controls
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
step_size = screen_height /  ( max-min );

// perform animation
var duration = 0.00625;
for (var i = 0; i < dataset.length - 40; i++ ) {
    // +300 is for margin at bottom
    tl1.to(p1, duration, { bottom: (dataset[i].f-min) * step_size + bottom_margin, width:(dataset[i].a*300), height:(dataset[i].a*300), borderRadius: ((dataset[i].a*300)/2) })
    tl2.to(p2, duration, { bottom: (dataset[i+10].f-min) * step_size + bottom_margin, width:(dataset[i+10].a*300), height:(dataset[i+10].a*300), borderRadius: ((dataset[i+10].a*300)/2) })
    tl3.to(p3, duration, { bottom: (dataset[i+20].f-min) * step_size + bottom_margin, width:(dataset[i+20].a*300), height:(dataset[i+20].a*300), borderRadius: ((dataset[i+20].a*300)/2) })
    tl4.to(p4, duration, { bottom: (dataset[i+30].f-min) * step_size + bottom_margin, width:(dataset[i+30].a*300), height:(dataset[i+30].a*300), borderRadius: ((dataset[i+30].a*300)/2) })
    tl5.to(p5, duration, { bottom: (dataset[i+40].f-min) * step_size + bottom_margin, width:(dataset[i+40].a*300), height:(dataset[i+40].a*300), borderRadius: ((dataset[i+40].a*300)/2) })
}

// fade out all the dots
tl1.to(p1, 2, { opacity: 0, bottom: 0 });
tl2.to(p2, 2, { opacity: 0, bottom: 0 });
tl3.to(p3, 2, { opacity: 0, bottom: 0 });
tl4.to(p4, 2, { opacity: 0, bottom: 0 });
tl5.to(p5, 2, { opacity: 0, bottom: 0 });

// Initialize Howl with music file
var audio = new Howl({
  urls: ['music.wav']
});

/*
    Define function for starting and stopping
    the animation
*/
function start() {
    tl1.play();
    tl2.play();
    tl3.play();
    tl4.play();
    tl5.play();
    audio.play();
}

function stop() {
    tl1.pause();    tl1.seek(0);
    tl2.pause();    tl2.seek(0);
    tl3.pause();    tl3.seek(0);
    tl4.pause();    tl4.seek(0);
    tl5.pause();    tl5.seek(0);
    audio.stop();
}
