function createObserver(targetElement, id, callback_url, description, visibility_callback = () => {}) {

    const callback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                visibility_callback(entry.target, description)
                setTimeout(async function() {
                    callback_url = new URL(callback_url)
                    callback_url.search = new URLSearchParams({
                        id: id,
                        metric_type: "visibility",
                        description
                    });
                    await fetch(callback_url);
                });
                observer.unobserve(entry.target);
            }
        });
    };
    const observer = new IntersectionObserver(callback, {
        threshold: 0.1
    });
    observer.observe(targetElement);

}

class ElementViewTracking {

    constructor(id, callback_url) {
        this._id = id;
        this._callback_url = callback_url;
    }

    visibility(dom_selector, description, visibility_callback = () => {}) {

        var targetElement = document.querySelector(dom_selector)
        if (targetElement) {
            createObserver(targetElement, this._id, this._callback_url, description, visibility_callback)
        }
        else {
            window.addEventListener("load", () => {
                var targetElement = document.querySelector(dom_selector)
                createObserver(targetElement, this._id, this._callback_url, description, visibility_callback)
            })
        }

        return this;
    }
}

function tracking(id, page_access_description, callback_url) {
    description = page_access_description || location.hostname.replace(/\\/g, "")
    if (callback_url) {
        setTimeout(async function() {
            callback_url = new URL(callback_url)
            callback_url.search = new URLSearchParams({
                id: id,
                metric_type: "page_access",
                description: description
            });
            await fetch(callback_url);
        });
    }

    return new ElementViewTracking(id, callback_url);
}
