let img__slider = document.getElementsByClassName('show');
img__slider[0].classList.add('active')

var input = document.getElementById("but");
var input2 = document.getElementById("buto");

let etape = 0;

let nbr__img = img__slider.length;

let suivant = document.querySelector('.but');

function enleverActiveImages() {
    for(let i = 0 ; i < nbr__img ; i++) {
        img__slider[i].classList.remove('active');
    }
}

suivant.addEventListener('click', function() {
    etape++;
    if(etape === nbr__img) {
        input.style.display = "none";
        input2.style.display = "block"
        
    }
    if(etape < nbr__img) {
        enleverActiveImages();
        img__slider[etape].classList.add('active');
    }
})