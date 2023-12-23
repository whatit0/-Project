import React, { useState } from "react";
// import { Document, Page } from "react-pdf";
import sampleImage1 from "./pamphlet.png";
import left from "./left.png";
import right from "./right.png";
import file from "./ppt.pdf";

import { Document, Page, pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/legacy/build/pdf.worker.min.js`;

function Report() {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  const goToPreviousPage = () => {
    if (pageNumber > 1) {
      setPageNumber(pageNumber - 1);
    }
  };

  const goToNextPage = () => {
    if (pageNumber < numPages) {
      setPageNumber(pageNumber + 1);
    }
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center", padding:"0 2%", position:"relative" }}>
        <div>

          <Document file={file} onLoadSuccess={onDocumentLoadSuccess}>
            <Page
              pageNumber={pageNumber}
              renderAnnotationLayer={false}
              renderTextLayer={false}
            />
          </Document>

          <p style={{ fontSize: "24px", textAlign: "center", position:"absolute", backgroundColor:"#fff", bottom:"30px", left:"40%", padding:"10px" }}>
            <img
              src={left}
              alt="Previous"
              onClick={goToPreviousPage}
              style={{ cursor: "pointer", width: "30px", height: "30px" }}
            />
            <span style={{ margin: "0 10px",  fontSize: "25px" }}>
              Page {pageNumber} of {numPages}
            </span>
            <img
              src={right}
              alt="Next"
              onClick={goToNextPage}
              style={{ cursor: "pointer", width: "30px", height: "30px" }}
            />
          </p>
        </div>
      </div>
      
      <div style={{ marginTop: '70px' }}>
        <img
          src={sampleImage1}
          alt="Sample Image 1"
          style={{ maxWidth: "100%", height: "auto" }}
        />
      </div>
    </div>
  );
}

export default Report;
