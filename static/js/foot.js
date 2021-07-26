window.onload = function() {
    let footer = document.querySelector('footer');       
  
    if (footer.offsetTop < document.documentElement.clientHeight - footer.offsetHeight) {
        footer.classList.add('fixed-bottom');        
    } else {
        footer.classList.remove('fixed-bottom');
    }
}
