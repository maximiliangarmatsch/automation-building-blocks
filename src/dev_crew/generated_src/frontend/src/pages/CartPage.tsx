import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import axios from 'axios';

const CartPage: React.FC = () => {
    const [cartItems, setCartItems] = useState([]);

    useEffect(() => {
        axios.get('/api/cart')
            .then(response => {
                setCartItems(response.data);
            })
            .catch(error => {
                console.error('Error fetching cart items:', error);
            });
    }, []);

    const getTotalPrice = () => {
        return cartItems.reduce((total, item) => total + item.total_price, 0).toFixed(2);
    };

    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <div className='container mx-auto p-10'>
                <h1 className='text-4xl font-bold mb-6'>Cart</h1>
                <div className='bg-white p-6 rounded shadow'>
                    {cartItems.length === 0 ? (
                        <p>Your cart is empty.</p>
                    ) : (
                        <div>
                            {cartItems.map((item: any) => (
                                <div key={item.drawing_id} className='flex justify-between items-center mb-4'>
                                    <img src={item.image_url} alt={item.title} className='w-20 h-20 object-cover rounded' />
                                    <div className='flex-1 ml-4'>
                                        <h3 className='text-lg font-bold'>{item.title}</h3>
                                        <p className='text-sm'>${item.price} x {item.quantity}</p>
                                    </div>
                                    <p className='text-lg font-bold'>${item.total_price.toFixed(2)}</p>
                                </div>
                            ))}
                            <div className='flex justify-between items-center mt-6'>
                                <h2 className='text-2xl font-bold'>Total</h2>
                                <p className='text-2xl font-bold'>${getTotalPrice()}</p>
                            </div>
                            <button className='bg-green-500 text-white py-2 px-4 rounded mt-4'>Proceed to Checkout</button>
                        </div>
                    )}
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default CartPage;