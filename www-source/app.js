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

/*
    CUSTOMIZE
*/
var bottom_margin = 50;
var top_margin = 50;
var amp_scale_factor = 20;


/*
    DYNAMICALLY CALCULATE PROPER VALUES
*/

// Get the screen size
var screen_height = window.innerHeight - bottom_margin - top_margin;        // controls
var screen_width = window.innerWidth;

// Find maximum and minimum frequency
var max_freq = 0;
var min_freq = 1000000;
for( var i = 0; i < dataset.length; i++ ) {
    var o = dataset[i];
    if( o.f > max_freq ) max_freq = o.f;
    if( o.f < min_freq ) min_freq = o.f;
}

// Find maximum and minimum amplitude
var max_amp = 0;
var min_amp = 1000000;
for( var i = 0; i < dataset.length; i++ ) {
    var o = dataset[i];
    if( o.a > max_amp ) max_amp = o.a;
    if( o.a < min_amp ) min_amp = o.a;
}

// Normalize amplitude by dividing with max_amp
for( var i = 0; i < dataset.length; i++ ) {
    dataset[i].a = dataset[i].a / max_amp;
}

// Calculate step size
freq_step_size = screen_height /  ( max_freq-min_freq );

// calculate duration
var duration = music_duration / dataset.length;

/*
    ANIMATION
*/

for (var i = 0; i < dataset.length - 40; i++ ) {
    tl1.to(p1, duration, {
        bottom: (dataset[i].f - min_freq) * freq_step_size,
        width: dataset[i].a * amp_scale_factor,
        height: dataset[i].a * amp_scale_factor,
        borderRadius: (dataset[i].a * amp_scale_factor) / 2
    });
    tl2.to(p2, duration, {
        bottom: (dataset[i+10].f - min_freq) * freq_step_size,
        width: dataset[i+10].a * amp_scale_factor,
        height: dataset[i+10].a * amp_scale_factor,
        borderRadius: (dataset[i+10].a * amp_scale_factor) / 2
    });
    tl3.to(p3, duration, {
        bottom: (dataset[i+20].f - min_freq) * freq_step_size,
        width: dataset[i+20].a * amp_scale_factor,
        height: dataset[i+20].a * amp_scale_factor,
        borderRadius: (dataset[i+20].a * amp_scale_factor) / 2
    });
    tl4.to(p4, duration, {
        bottom: (dataset[i+30].f - min_freq) * freq_step_size,
        width: dataset[i+30].a * amp_scale_factor,
        height: dataset[i+30].a * amp_scale_factor,
        borderRadius: (dataset[i+30].a * amp_scale_factor) / 2
    });
    tl5.to(p5, duration, {
        bottom: (dataset[i+40].f - min_freq) * freq_step_size,
        width: dataset[i+40].a * amp_scale_factor,
        height: dataset[i+40].a * amp_scale_factor,
        borderRadius: (dataset[i+40].a * amp_scale_factor) / 2
    });
}

// Fade out all the dots
tl1.to(p1, 2, { opacity: 0, bottom: 0 });
tl2.to(p2, 2, { opacity: 0, bottom: 0 });
tl3.to(p3, 2, { opacity: 0, bottom: 0 });
tl4.to(p4, 2, { opacity: 0, bottom: 0 });
tl5.to(p5, 2, { opacity: 0, bottom: 0 });


/*
    AUDIO
*/
// Initialize Howl with music file
var audio = new Howl({
  urls: ['music.wav']
});


/*
    START AND STOP CONTROL
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
