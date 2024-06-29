
const charLimit = 100000;

function display(text) {
    header = document.createElement("div");
    header.style.backgroundColor = "#d18ee2";
    header.style.padding = "5px";

    tldr = document.createElement("p");
    tldr.textContent = text;
    tldr.style.margin = "10px 100px";
    tldr.style.fontSize = "medium";
    tldr.style.color = "white";
    tldr.style.textAlign = "center";
    tldr.style.fontFamily = "Verdana, Geneva, sans-serif";
    header.appendChild(tldr);

    document.body.parentNode.insertBefore(header, document.body);
}

function summarize(text) {
    chrome.storage.sync.get('apiKey', key => {
        options = {
            "method": "POST",
            "headers": {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": "Bearer " + key.apiKey,
                "Request-Source": "sandbox-condense"
            },

            "body": JSON.stringify({
                "message": text,
                "preamble": "Generate a summary of this webpage: ",
                "temperature": 0.1
            })
        };

        fetch('https://api.cohere.ai/v1/chat', options)
            .then((response) => response.json())
            .then((response) => {
                if (response.text === undefined) {
                    display("There was an error: " + response.message);
                } else {
                    display("tl;dr: " + response.text);
                }
            });
    });
}

function isHidden(el) {
    var style = window.getComputedStyle(el);
    return ((style.display === 'none') || (style.visibility === 'hidden'))
}

function getVisibleText() {

    var body = document.querySelector('body')
    if (document.querySelector('#content')) {
        body = document.querySelector('#content');
    }
    if (document.main) {
        body = document.querySelector('main');
    }
    var allTags = body.getElementsByTagName('*');

    let visibleText = [];
    var nChars = 0;
    for (var i = 0, max = allTags.length; i < max; i++) {
        var elem = allTags[i];
        if (!isHidden(elem)) {

            var text = $(elem).contents().filter(function() {
                return this.nodeType == Node.TEXT_NODE;
            });
            if (text === undefined || text.length == 0) {
                continue;
            }
            text = text[0].nodeValue
            nChars += text.length + 1; 
            if (nChars < charLimit) {
                visibleText.push(text);
            } else {
                break
            }
        }
    }
    return visibleText.join('\n');
}

function main() {
    chrome.storage.sync.get('apiKey', key => {
        if (key.apiKey === undefined) {
            display("Please set an API key in Condense > Options. You can get one from https://dashboard.cohere.ai/api-keys");
        } else {
            const truncatedVisibleText = getVisibleText()
            console.log(truncatedVisibleText);
            summarize(truncatedVisibleText);
        }
    });
}

main()