import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ShopGrid: React.FC = () => {
    const [drawings, setDrawings] = useState([]);

    useEffect(() => {
        axios.get('/api/drawings')
            .then(response => {
                setDrawings(response.data);
            })
            .catch(error => {
                console.error('Error fetching drawings:', error);
            });
    }, []);

    return (
        <div className='grid grid-cols-4 gap-4'>
            {drawings.map((drawing: any) => (
                <div key={drawing.id} className='drawing-card bg-white p-4 rounded shadow'>
                    <img src={drawing.image_url} alt={drawing.title} className='w-full h-40 object-cover rounded' />
                    <h3 className='text-lg font-bold mt-2'>{drawing.title}</h3>
                    <p className='text-sm mt-1'>${drawing.price}</p>
                </div>
            ))}
        </div>
    );
};

export default ShopGrid;