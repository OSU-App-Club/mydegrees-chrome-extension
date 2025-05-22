// <use xlink:href="#ds-icon-circle"></use>
// <use xlink:href="#ds-icon-check-feedback"></use>
// <use xlink:href="#ds-icon-partial"></use>

// Options for the observer (which mutations to observe)
const config = { attributes: true, childList: true, subtree: true };

// Callback function to execute when mutations are observed
const callback: MutationCallback = mutationList => {
    for (const _ of mutationList) {
        const checks = document.querySelectorAll('use[*|href="#ds-icon-circle"]');
        console.log('checks', checks);
    }
};

// Create an observer instance linked to the callback function
const observer = new MutationObserver(callback);

// Start observing the target node for configured mutations
observer.observe(document, config);
