import React from 'react';

const CategoriesSection: React.FC = () => {
    return (
        <div className='categories p-10'>
            <h2 className='text-2xl font-bold mb-4'>Categories</h2>
            <div className='grid grid-cols-3 gap-4'>
                <div className='category bg-light-grey p-6 text-center rounded'>
                    <h3 className='text-xl'>Portraits</h3>
                </div>
                <div className='category bg-light-grey p-6 text-center rounded'>
                    <h3 className='text-xl'>Landscapes</h3>
                </div>
                <div className='category bg-light-grey p-6 text-center rounded'>
                    <h3 className='text-xl'>Abstract</h3>
                </div>
            </div>
        </div>
    );
};

export default CategoriesSection;