window.onload = function(){
    var b=document.querySelector('body')
    b.onmousemove = (e) => {
      const x = e.pageX
      const y = e.pageY
      b.style.setProperty('--x', `${x/100}`)
      b.style.setProperty('--y', `${y/100}`)
      b.style.setProperty('--s', `${x/20}deg`)
    }
}