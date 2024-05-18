# Search box

<input id="criteriaText" name="criteriaText" class="form-control" type="text" value="" maxlength="100">

# Search button

<button type="submit" name="_eventId_search" class="btn btn-primary btn-front-page" onclick="triggerLoadModal();">
                                     Hae</button>

# Download PDF Button

<button type="submit" name="_eventId_createElectronicTRExtract" class="btn btn-primary btn-block btn-cart-internal">
                                        Avaa maksuton kaupparekisteriote<svg class="feather prh-icon icon-small" aria-hidden="false"><use href="/novus/resources/images/feather-sprite.svg#file"></use></svg></button>


# second tab link

<a href="/novus/reportdisplay" target="_blank">Jos ote ei avaudu automaattisesti, voit avata sen tästä linkistä.<svg class="feather prh-icon--white external-link-icon" aria-label=", To prh.fi website" role="img">
                    <use href="resources/images/feather-sprite.svg#external-link"></use></svg></a>


# Download PDF Button inside the pdf viewer
<cr-icon-button id="download" iron-icon="cr:file-download" aria-label="Download" title="Download" aria-haspopup="false" role="button" tabindex="0" aria-disabled="false"></cr-icon-button>

<div id="icon">
  <div id="maskedImage"></div>
<iron-icon></iron-icon></div>

## js path

document.querySelector("#viewer").shadowRoot.querySelector("#toolbar").shadowRoot.querySelector("#downloads").shadowRoot.querySelector("#download")

## selector
#download

## xpath
//*[@id="download"]
## full path
/html/body/pdf-viewer//viewer-toolbar//div/div[3]/viewer-download-controls//cr-icon-button