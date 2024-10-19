import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const AboutUsPage: React.FC = () => {
    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <div className='container mx-auto p-10'>
                <h1 className='text-4xl font-bold mb-6'>About Us</h1>
                <p>Our company history, mission statement, and team members.</p>
                <div className='grid grid-cols-3 gap-4 mt-6'>
                    <div className='team-member bg-white p-4 rounded shadow'>
                        <img src='/path/to/image.jpg' alt='Team Member' className='w-full h-40 object-cover rounded' />
                        <h3 className='text-lg font-bold mt-2'>John Doe</h3>
                        <p className='text-sm'>CEO</p>
                    </div>
                    <div className='team-member bg-white p-4 rounded shadow'>
                        <img src='/path/to/image.jpg' alt='Team Member' className='w-full h-40 object-cover rounded' />
                        <h3 className='text-lg font-bold mt-2'>Jane Smith</h3>
                        <p className='text-sm'>CTO</p>
                    </div>
                    <div className='team-member bg-white p-4 rounded shadow'>
                        <img src='/path/to/image.jpg' alt='Team Member' className='w-full h-40 object-cover rounded' />
                        <h3 className='text-lg font-bold mt-2'>Emily Johnson</h3>
                        <p className='text-sm'>COO</p>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default AboutUsPage;