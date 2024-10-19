import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import axios from 'axios';

const DrawingDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [drawing, setDrawing] = useState<any>(null);

    useEffect(() => {
        axios.get(`/api/drawings/${id}`)
            .then(response => {
                setDrawing(response.data);
            })
            .catch(error => {
                console.error('Error fetching drawing details:', error);
            });
    }, [id]);

    if (!drawing) {
        return <div>Loading...</div>;
    }

    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <div className='container mx-auto p-10'>
                <div className='flex'>
                    <div className='w-1/2'>
                        <img src={drawing.image_urls[0]} alt={drawing.title} className='w-full h-auto object-cover rounded' />
                    </div>
                    <div className='w-1/2 pl-10'>
                        <h1 className='text-4xl font-bold mb-4'>{drawing.title}</h1>
                        <p className='text-xl mb-4'>${drawing.price}</p>
                        <p className='mb-4'>{drawing.description}</p>
                        <button className='bg-green-500 text-white py-2 px-4 rounded'>Add to Cart</button>
                    </div>
                </div>
                <div className='mt-10'>
                    <h2 className='text-2xl font-bold mb-4'>Related Drawings</h2>
                    {/* Related drawings section */}
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default DrawingDetailPage;