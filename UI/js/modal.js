const btn = document.getElementsByClassName('button-modal');

for (let i = 0; i < btn.length; i += 1) {
  const thisBtn = btn[i];
  thisBtn.addEventListener('click', function () {
    const modal = document.getElementById(this.dataset.modal);
    modal.style.display = 'block';
  }, false);
}

// Get the <span> element that closes the modal
const span = document.getElementsByClassName('close');

for (let i = 0; i < span.length; i += 1) {
  const thisSpan = span[i];
  const closeModalButton = () => {
    const modal = document.getElementsByClassName('modal');
    for (let j = 0; j < modal.length; j += 1) {
      modal[j].style.display = 'none';
    }
  };
  thisSpan.addEventListener('click', closeModalButton, false);
}

// When the user clicks anywhere outside of the modal, close it
const modal = document.getElementsByClassName('modal');
const closeModal = (event) => {
  for (let k = 0; k < modal.length; k += 1) {
    if (event.target === modal[k]) {
      modal[k].style.display = 'none';
    }
  }
};
window.addEventListener('click', event => closeModal(event));
