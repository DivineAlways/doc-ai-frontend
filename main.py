// pages/index.js
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [userId, setUserId] = useState(() => {
    let id = localStorage.getItem('user_id');
    if (!id) {
      id = 'user_' + Math.random().toString(36).substring(2, 10);
      localStorage.setItem('user_id', id);
    }
    return id;
  });

  const handleUpload = async () => {
    if (!file) return alert('Please select a PDF file to upload.');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/upload/`, formData);
      alert(res.data.message);
    } catch (err) {
      console.error(err);
      alert('Upload failed.');
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/query/`, {
        query,
        user_id: userId
      });
      setResponse(res.data.response);
    } catch (err) {
      console.error(err);
      alert('Search failed.');
    }
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-4">🧠 Doc AI Assistant</h1>

      <section className="mb-6">
        <label className="block mb-2 font-semibold">Upload a PDF</label>
        <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button
          onClick={handleUpload}
          className="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
        >
          Upload
        </button>
      </section>

      <section className="mb-6">
        <label className="block mb-2 font-semibold">Ask a Question</label>
        <input
          type="text"
          className="w-full p-2 text-black rounded"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. What is the summary of this document?"
        />
        <button
          onClick={handleSearch}
          className="mt-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded"
        >
          Search
        </button>
      </section>

      {response && (
        <section className="mt-6 p-4 bg-gray-800 rounded">
          <h2 className="text-xl font-semibold mb-2">AI Response:</h2>
          <p>{response}</p>
        </section>
      )}
    </main>
  );
}
