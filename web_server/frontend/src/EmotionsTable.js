
import React, { useState, useEffect } from "react";

const EmotionsTable = ({ emotion }) => {
  // State to store the images
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch the images for the specified emotion
  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await fetch(`http://localhost:3000/images/${emotion}`);
        
        // If response is not OK, throw an error
        if (!response.ok) {
            console.log("error")
          throw new Error("Failed to fetch images");
        }

        const data = await response.json();
        
        // Set images in state, but only the first 8
        setImages(data.slice(0, 8));  // Get the first 8 images
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, [emotion]);  // Dependency on emotion to re-fetch when it changes

  // If data is still loading, display loading message
  if (loading) {
    return <div>Loading...</div>;
  }

  // If there is an error fetching data, show an error message
  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>{emotion.charAt(0).toUpperCase() + emotion.slice(1)} People</h2>
      <div className="image-gallery">
        {images.map((img, index) => (
          <div key={index} className="image-item">
            <img
              src={`data:image/${img.image_type};base64,${img.image}`}
              alt={`${emotion} ${index + 1}`}
              style={{ width: "150px", height: "auto", margin: "10px" }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmotionsTable;