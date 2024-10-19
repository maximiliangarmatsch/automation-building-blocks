import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const ContactUsPage: React.FC = () => {
    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <div className='container mx-auto p-10'>
                <h1 className='text-4xl font-bold mb-6'>Contact Us</h1>
                <form className='bg-white p-6 rounded shadow'>
                    <div className='grid grid-cols-2 gap-4'>
                        <input type='text' name='name' placeholder='Name' className='p-2 border rounded' required />
                        <input type='email' name='email' placeholder='Email' className='p-2 border rounded' required />
                    </div>
                    <textarea name='message' placeholder='Message' className='p-2 border rounded mt-4' rows={5} required></textarea>
                    <button type='submit' className='bg-blue-500 text-white py-2 px-4 rounded mt-4'>Send Message</button>
                </form>
                <div className='mt-10'>
                    <h2 className='text-2xl font-bold mb-4'>Our Office</h2>
                    <p>123 Art Street, Gallery City, Artland, 12345</p>
                    <iframe src='https://www.google.com/maps/embed?...' className='w-full h-64 mt-4' title='Our Office Location'></iframe>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default ContactUsPage;