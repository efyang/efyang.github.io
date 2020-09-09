const observeElementInViewport = window.observeElementInViewport.observeElementInViewport
const viewport = document.querySelector(null)
// element whose visibility we want to track
const targets = document.querySelectorAll('video')

// only play videos that are in viewport
const inHandler = (entry, unobserve, targetEl) => targetEl.play()
const outHandler = (entry, unobserve, targetEl) => targetEl.pause()

targets.forEach((target) => {
    observeElementInViewport(target, inHandler, outHandler, {
          viewport,
          // decrease viewport top by 100px
          // similar to this, modRight, modBottom and modLeft exist
          modTop: '-50px',

          // threshold tells us when to trigger the handlers.
          // a threshold of 90 means, trigger the inHandler when atleast 90%
          // of target is visible. It triggers the outHandler when the amount of
          // visible portion of the target falls below 90%.
          // If this array has more than one value, the lowest threshold is what
          // marks the target as having left the viewport
          threshold: [0]
        })
})
