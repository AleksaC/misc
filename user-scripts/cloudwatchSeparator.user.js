// ==UserScript==
// @match *://*.console.aws.amazon.com/cloudwatch/*
// ==/UserScript==

let iframeMutationObserver;

const rootMutationObserver = new MutationObserver((mutationRecords) => {
  for (const mutationRecord of mutationRecords) {
    if (mutationRecord.addedNodes.length > 0) {
      for (const node of mutationRecord.addedNodes) {
        if (node.nodeType !== Node.ELEMENT_NODE) continue;

        const iframe = node.querySelector("#microConsole-Logs");

        if (iframe && !iframeMutationObserver) {
          iframeMutationObserver = new MutationObserver((mutationRecords) => {
            for (const mutationRecord of mutationRecords) {
              if (mutationRecord.addedNodes.length > 0) {
                for (const node of mutationRecord.addedNodes) {
                  if (node.nodeType !== Node.ELEMENT_NODE) continue;

                  const cells = node.querySelectorAll(
                    "span.logs__log-events-table__cell"
                  );

                  if (cells.length) {
                    for (const cell of cells) {
                      if (cell.textContent.startsWith("REPORT RequestId:")) {
                        const table = iframe.contentDocument.body.querySelector(
                          "table"
                        );
                        const tableStyle = getComputedStyle(table);
                        if (tableStyle.borderCollapse === "separate") {
                          table.setAttribute(
                            "style",
                            "border-collapse: collapse;"
                          );
                        }

                        cell.parentNode.parentNode.parentNode.parentNode.setAttribute(
                          "style",
                          "border-bottom: 2px solid red;"
                        );
                      }
                    }
                  }
                }
              }
            }
          });

          iframeMutationObserver.observe(iframe.contentDocument.body, {
            childList: true,
            subtree: true,
          });
        }
      }
    }
  }
});

rootMutationObserver.observe(document.body, { childList: true, subtree: true });
