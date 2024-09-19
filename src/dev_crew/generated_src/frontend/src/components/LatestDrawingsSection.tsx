import React from 'react';

const LatestDrawingsSection: React.FC = () => {
    return (
        <div className='latest-drawings p-10'>
            <h2 className='text-2xl font-bold mb-4'>Latest Drawings</h2>
            <div className='grid grid-cols-4 gap-4'>
                {/* Example drawing cards */}
                <div className='drawing-card bg-white p-4 rounded shadow'>
                    <img src='/path/to/image.jpg' alt='Drawing' className='w-full h-40 object-cover rounded' />
                    <h3 className='text-lg font-bold mt-2'>Drawing Title</h3>
                    <p className='text-sm mt-1'>$100</p>
                </div>
                {/* Add more drawing cards here */}
            </div>
        </div>
    );
};

export default LatestDrawingsSection;