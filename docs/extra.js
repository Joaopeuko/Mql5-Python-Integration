function cleanupClipboardText(targetSelector) {
    const targetElement = document.querySelector(targetSelector);

    // exclude "Generic Prompt" and "Generic Output" spans from copy
    const excludedClasses = ["gp", "go"];

    const clipboardText = Array.from(targetElement.childNodes)
      .filter(
        (node) =>
          !excludedClasses.some((className) =>
            node?.classList?.contains(className),
          ),
      )
      .map((node) => node.textContent)
      .filter((s) => s != "");
    return clipboardText.join("").trim();
  }

  // Sets copy text to attributes lazily using an Intersection Observer.
  function setCopyText() {
    // The `data-clipboard-text` attribute allows for customized content in the copy
    // See: https://www.npmjs.com/package/clipboard#copy-text-from-attribute
    const attr = "clipboardText";
    // all "copy" buttons whose target selector is a <code> element
    const elements = document.querySelectorAll(
      'button[data-clipboard-target$="code"]',
    );
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        // target in the viewport that have not been patched
        if (
          entry.intersectionRatio > 0 &&
          entry.target.dataset[attr] === undefined
        ) {
          entry.target.dataset[attr] = cleanupClipboardText(
            entry.target.dataset.clipboardTarget,
          );
        }
      });
    });

    elements.forEach((elt) => {
      observer.observe(elt);
    });
  }

  // Show sponsor popup on first visit
  function showSponsorPopup() {
    // Check if user has seen the popup before
    if (!localStorage.getItem('mqpy_sponsor_popup_shown')) {
      // Create popup container
      const popup = document.createElement('div');
      popup.className = 'sponsor-popup';

      // Create popup content
      popup.innerHTML = `
        <div class="sponsor-popup-content">
          <div class="sponsor-popup-header">
            <h2>Support MQPy Development</h2>
            <button class="sponsor-popup-close">&times;</button>
          </div>
          <div class="sponsor-popup-body">
            <p>Thank you for using MQPy! This project is free and open-source, developed in my free time.</p>
            <p>If you find MQPy useful, please consider supporting its development:</p>
            <div class="sponsor-popup-buttons">
              <a href="https://github.com/sponsors/Joaopeuko" class="sponsor-popup-button primary" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="currentColor"/></svg>
                Become a Sponsor
              </a>
            </div>
            <div class="sponsor-popup-footer">
              <label>
                <input type="checkbox" id="sponsor-popup-dont-show"> Don't show this message again
              </label>
            </div>
          </div>
        </div>
      `;

      // Add popup to body
      document.body.appendChild(popup);

      // Show popup with animation
      setTimeout(() => {
        popup.classList.add('active');
      }, 1000);

      // Close button event
      const closeBtn = popup.querySelector('.sponsor-popup-close');
      closeBtn.addEventListener('click', () => {
        popup.classList.remove('active');

        // Check if "don't show again" is checked
        const dontShowAgain = document.getElementById('sponsor-popup-dont-show').checked;
        if (dontShowAgain) {
          localStorage.setItem('mqpy_sponsor_popup_shown', 'true');
        }

        // Remove popup after animation
        setTimeout(() => {
          popup.remove();
        }, 300);
      });
    }
  }

  // Using the document$ observable is particularly important if you are using instant loading since
  // it will not result in a page refresh in the browser
  // See `How to integrate with third-party JavaScript libraries` guideline:
  // https://squidfunk.github.io/mkdocs-material/customization/?h=javascript#additional-javascript
  document$.subscribe(function () {
    setCopyText();
    showSponsorPopup();
  });
