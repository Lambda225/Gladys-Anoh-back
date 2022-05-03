const burger = document.querySelector('nav .burger')
const menuMobile = document.querySelector('.responsive_menu')
const body = document.querySelector('body')
const nav = document.querySelector('header nav')
let i = false

burger.addEventListener('click',() =>{
    if(i){
        menuMobile.style.top = '-100%'
        burger.innerHTML = '<i class="fa-solid fa-bars"></i>'
        body.style.overflow = 'visible'
        nav.style.background = 'transparent'
        i = false
    }else{
        menuMobile.style.top = '0'
        burger.innerHTML = '<i class="fa-solid fa-xmark"></i>'
        body.style.overflow = 'hidden'
        nav.style.background = 'white'
        i = true    
    }
})