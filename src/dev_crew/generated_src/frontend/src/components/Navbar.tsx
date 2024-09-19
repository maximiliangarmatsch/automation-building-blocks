import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    return (
        <nav className='bg-blue-500 p-4'>
            <div className='container mx-auto flex justify-between'>
                <div className='text-white text-lg font-bold'>Art Gallery</div>
                <div className='space-x-4'>
                    <Link to='/' className='text-white'>Home</Link>
                    <Link to='/shop' className='text-white'>Shop</Link>
                    <Link to='/about' className='text-white'>About Us</Link>
                    <Link to='/contact' className='text-white'>Contact Us</Link>
                    <Link to='/cart' className='text-white'>Cart</Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;