var btn = document.getElementsByClassName('button-modal');

for (var i = 0; i < btn.length; i++) {
  var thisBtn = btn[i];
  thisBtn.addEventListener('click', function(){
    var modal = document.getElementById(this.dataset.modal);
    modal.style.display = 'block';
    
}, false);}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName('close');

for (var i = 0; i < span.length; i++) {
    var thisSpan = span[i];
    thisSpan.addEventListener('click', function(){
      var modal = document.getElementsByClassName('modal');
      for (var j = 0; j < modal.length; j++) {
        modal[j].style.display = 'none';
      }
  }, false);}

// When the user clicks anywhere outside of the modal, close it
var modal = document.getElementsByClassName('modal');

window.onclick = function(event) {
    for (var k = 0; k < modal.length; k++){
        if (event.target === modal[k]) {
            modal[k].style.display = 'none';
        }
    }
}
