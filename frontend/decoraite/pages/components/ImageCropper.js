// components/ImageCropper.js
import React, { useState, useRef } from 'react';
import { useEffect } from 'react';
import { Stage, Layer, Image, Rect, Transformer } from 'react-konva';
import useImage from 'use-image';

const ImageCropper = ({ src }) => {

  useEffect(() => {
    console.log("SOURCE")
    console.log(src)
  })
  const [image] = useImage(src);
  const [rect, setRect] = useState({ x: 50, y: 50, width: 200, height: 100 });
  const rectRef = useRef();
  const trRef = useRef();

  const onDragEnd = (e) => {
    setRect({
      ...rect,
      x: e.target.x(),
      y: e.target.y(),
    });
  };

  const onTransformEnd = (e) => {
    // transformer is changing scale
    const node = rectRef.current;
    const scaleX = node.scaleX();
    const scaleY = node.scaleY();

    // we will reset it back
    node.scaleX(1);
    node.scaleY(1);
    setRect({
      x: node.x(),
      y: node.y(),
      // set minimal value
      width: Math.max(5, node.width() * scaleX),
      height: Math.max(node.height() * scaleY, 5)
    });
  };

  return (
    <Stage width={window.innerWidth} height={window.innerHeight}>
      <Layer>
        <Image image={image} />
        <Rect
          fill='rgba(0,0,255,0.5)'
          {...rect}
          draggable
          onDragEnd={onDragEnd}
          onTransformEnd={onTransformEnd}
          ref={rectRef}
        />
        <Transformer
          ref={trRef}
          boundBoxFunc={(oldBox, newBox) => {
            // limit resize
            if (newBox.width < 5 || newBox.height < 5) {
              return oldBox;
            }
            return newBox;
          }}
          node={rectRef.current}
          enabledAnchors={['top-left', 'top-right', 'bottom-left', 'bottom-right']}
          keepRatio={false}
        />
      </Layer>
    </Stage>
  );
};

export default ImageCropper;
