// components/ImageUploadWithModal.js
import React, { useState, useEffect } from 'react';
import ImageCropper from './ImageCropper';

const ImageUploadWithModal = () => {
  const [open, setOpen] = useState(false);
  const [imageSrc, setImageSrc] = useState("");

  const onFileChange = async (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      let imageDataUrl = await readFile(file);
  
      console.log(imageDataUrl);
      setImageSrc(imageDataUrl);
      setOpen(true); // Open the modal after setting the image source
    }
  };
  

  const readFile = (file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve(reader.result);
      };
      reader.readAsDataURL(file);
    });
  };

  
  const closeModal = () => {
    setOpen(false);
  };


  useEffect(() => {
    console.log("IMAGE SRC")
    console.log(imageSrc)
  }, [imageSrc]) 

  return (
    <div>
      <input type="file" accept="image/*" onChange={onFileChange} />
      {open && (
        <div className="modal">
          <div className="modal-content">
            <span className="close-button" onClick={closeModal}>&times;</span>
            {imageSrc && imageSrc.length > 0 &&  <ImageCropper src={imageSrc} />}
          </div>
        </div>
      )}
      <style jsx global>{`
        .modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }
        .modal-content {
          position: relative;
          width: 80%;
          max-width: 900px;
          background: white;
          padding: 20px;
        }
        .close-button {
          position: absolute;
          top: 10px;
          right: 20px;
          font-size: 1.5em;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
};

export default ImageUploadWithModal;
