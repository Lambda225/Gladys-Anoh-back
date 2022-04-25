 //Slider
 const suivants = document.querySelectorAll(".suivant");
 const precedants = document.querySelectorAll(".precedant")
 const container= document.querySelector(".contener_slider .slider");
 const ItemNo = container.querySelectorAll(".contener_slider .slider .item").length;
 let clickitem = 0
 
 suivants.forEach((suivant) =>{
     suivant.addEventListener("click", () => {
         clickitem++;
         if(ItemNo - (1 + clickitem) >= 0){
             container.style.transform = `translateX(${
                 container.computedStyleMap().get("transform")[0].x.value
                 - 320}px)`;
         }else{
             container.style.transform = "translateX(0)";
             clickitem = 0;
         }
     });
 })

 precedants.forEach((precedant) =>{
     precedant.addEventListener("click", () => {
         clickitem--;
         if(ItemNo - (6 + clickitem) < 0){
             container.style.transform = `translateX(${
                 container.computedStyleMap().get("transform")[0].x.value
                 + 320}px)`;
         }else{
             container.style.transform = `translateX(${
                 container.computedStyleMap().get("transform")[0].x.value
                 - (4 *320)}px)`;
             clickitem = 4;
         }
     });
 })

 //Scroll down

 const smoothScroll = (targets,duration) =>{
     const target = document.querySelector(targets);
     const targetPosition = target.getBoundingClientRect().top;
     const startPosition = window.pageYOffset;
     var distance = targetPosition - startPosition;
     var startTime = null;
     
     const animation = (currentTime) => {
         if(startTime === null){
             startTime = currentTime;
         }
         let timeElapsed = currentTime - startTime;
         let run = ease(timeElapsed,startPosition,distance,duration);
         window.scrollTo(0,run);
         if(timeElapsed < duration){
             requestAnimationFrame(animation);
         }
     }
     
     const ease = (t, b, c, d) => {
         t /= d /2;
         if (t < 1) {
             return c / 2 * t * t + b;
         }
         t--;
         return -c / 2 * (t * (t - 2) - 1) + b;
     }

     requestAnimationFrame(animation);
 }
 
 const btnDown = document.querySelector('.text_header a')
 btnDown.addEventListener('click',(e) =>{
     e.preventDefault()
     smoothScroll('.articles',1000)
 })