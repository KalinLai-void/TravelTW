const showInfoButtons = document.querySelectorAll('[data-modal-target]')
const closeInfoButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('popup-window')

showInfoButtons.forEach(element => {
    element.addEventListener('click', () => {
        const window = document.querySelector(element.dataset.modalTarget)
        openModal(window)
    })
});

closeInfoButtons.forEach(element => {
    element.addEventListener('click', () => {
        const window = element.closest('.course-detail')
        closeModal(window)
    })
});

function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}