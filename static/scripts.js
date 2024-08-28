function nextStep(currentStep) {
    console.log(`Current Step: ${currentStep}`);
    const currentStepElement = document.getElementById(`step${currentStep}`);
    const nextStepElement = document.getElementById(`step${currentStep + 1}`);
    
    console.log(`Current Step Element:`, currentStepElement);
    console.log(`Next Step Element:`, nextStepElement);
    
    if (currentStepElement.checkValidity()) {
        currentStepElement.classList.remove('active');
        nextStepElement.classList.add('active');
    } else {
        currentStepElement.reportValidity();
    }
}