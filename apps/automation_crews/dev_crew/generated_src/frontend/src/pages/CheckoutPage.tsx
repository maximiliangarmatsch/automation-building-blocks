import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import axios from 'axios';

const CheckoutPage: React.FC = () => {
    const [billingDetails, setBillingDetails] = useState({ name: '', address: '', city: '', country: '', postal_code: '' });
    const [paymentInfo, setPaymentInfo] = useState({ card_number: '', expiry_date: '', cvv: '' });
    const [message, setMessage] = useState('');

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setBillingDetails({ ...billingDetails, [name]: value });
    };

    const handlePaymentInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setPaymentInfo({ ...paymentInfo, [name]: value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        axios.post('/api/checkout', { billing_details: billingDetails, payment_info: paymentInfo })
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error('Error during checkout:', error);
                setMessage('An error occurred during checkout.');
            });
    };

    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <div className='container mx-auto p-10'>
                <h1 className='text-4xl font-bold mb-6'>Checkout</h1>
                <form onSubmit={handleSubmit} className='bg-white p-6 rounded shadow'>
                    <h2 className='text-2xl font-bold mb-4'>Billing Details</h2>
                    <div className='grid grid-cols-2 gap-4'>
                        <input type='text' name='name' placeholder='Name' className='p-2 border rounded' value={billingDetails.name} onChange={handleInputChange} required />
                        <input type='text' name='address' placeholder='Address' className='p-2 border rounded' value={billingDetails.address} onChange={handleInputChange} required />
                        <input type='text' name='city' placeholder='City' className='p-2 border rounded' value={billingDetails.city} onChange={handleInputChange} required />
                        <input type='text' name='country' placeholder='Country' className='p-2 border rounded' value={billingDetails.country} onChange={handleInputChange} required />
                        <input type='text' name='postal_code' placeholder='Postal Code' className='p-2 border rounded' value={billingDetails.postal_code} onChange={handleInputChange} required />
                    </div>
                    <h2 className='text-2xl font-bold mt-6 mb-4'>Payment Information</h2>
                    <div className='grid grid-cols-3 gap-4'>
                        <input type='text' name='card_number' placeholder='Card Number' className='p-2 border rounded' value={paymentInfo.card_number} onChange={handlePaymentInputChange} required />
                        <input type='text' name='expiry_date' placeholder='Expiry Date (MM/YY)' className='p-2 border rounded' value={paymentInfo.expiry_date} onChange={handlePaymentInputChange} required />
                        <input type='text' name='cvv' placeholder='CVV' className='p-2 border rounded' value={paymentInfo.cvv} onChange={handlePaymentInputChange} required />
                    </div>
                    <button type='submit' className='bg-green-500 text-white py-2 px-4 rounded mt-4'>Place Order</button>
                </form>
                {message && <p className='mt-4 text-red-500'>{message}</p>}
            </div>
            <Footer />
        </div>
    );
};

export default CheckoutPage;