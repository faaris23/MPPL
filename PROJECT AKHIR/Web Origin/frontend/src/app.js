import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [image, setImage] = useState(null);
  const [platform, setPlatform] = useState('');
  const [style, setStyle] = useState('');
  const [result, setResult] = useState(null);

  const handleImageUpload = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('platform', platform);
    formData.append('style', style);

    try {
      const response = await axios.post('http://localhost:5000/api/generate', formData);
      setResult(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Image Caption Generator</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      <select onChange={(e) => setPlatform(e.target.value)}>
        <option value="">Select Platform</option>
        <option value="instagram">Instagram</option>
        <option value="tiktok">TikTok</option>
        <option value="youtube">YouTube</option>
      </select>
      <select onChange={(e) => setStyle(e.target.value)}>
        <option value="">Select Caption Style</option>
        <option value="cool">Cool</option>
        <option value="trendy">Trendy</option>
        <option value="horror">Horror</option>
      </select>
      <button onClick={handleSubmit}>Generate</button>

      {result && (
        <div>
          <h2>Generated Caption</h2>
          <p>{result.caption}</p>
          <h2>Generated Hashtags</h2>
          <p>{result.hashtags.join(', ')}</p>
        </div>
      )}
    </div>
  );
}

export default App;
