"use strict";


var canvas = document.getElementById('canvas-picker').getContext('2d');

// create an image object and get it’s source
var img = new Image();
img.src = '/static/img/color_wheel.png';

// copy the image to the canvas
function addImageToCanvas() {
    canvas.drawImage(img, 0, 0);
}

// $(document).ready(addImageToCanvas);
setTimeout(addImageToCanvas, 1000);

// // copy the image to the canvas
// $(img).load(function(){
//   canvas.drawImage(img,0,0);
// });

var colorHEX;

// http://www.javascripter.net/faq/rgbtohex.htm
function rgbToHex(R,G,B) {return toHex(R)+toHex(G)+toHex(B)}
function toHex(n) {
n = parseInt(n,10);
if (isNaN(n)) return "00";
n = Math.max(0,Math.min(n,255));
return "0123456789ABCDEF".charAt((n-n%16)/16)  + "0123456789ABCDEF".charAt(n%16);
}
$('#canvas-picker').click(function(event){
// getting user coordinates
var x = event.pageX - this.offsetLeft;
var y = event.pageY - this.offsetTop;
// getting image data and RGB values
var imgData = canvas.getImageData(x, y, 1, 1).data;
var R = imgData[0];
var G = imgData[1];
var B = imgData[2];
var rgb = R + ',' + G + ',' + B;
// convert RGB to HEX
var hex = rgbToHex(R,G,B);
colorHEX = '#'+hex;
// making the color the value of the input
$('#rgb input').val(rgb);
$('#hex input').val('#' + hex);
});



$(document).on('click', changeColor);

function changeColor(e) {
    console.log(colorHEX);
    $('#sample-box').css('background-color', colorHEX);
}


var opacity;

$(document).ready(function() {
    $('#opacity-range').change(updateValue);
});

function updateValue(e) {
    opacity = $('#opacity-range').val();
    $('#sample-box').css('opacity', opacity/100);
    $('#sample-box').html(opacity + '% opacity');
    console.log('changed value is ' + opacity);
}
