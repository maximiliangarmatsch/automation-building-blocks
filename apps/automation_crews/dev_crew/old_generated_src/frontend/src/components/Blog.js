import React from 'react';

function Blog() {
  return (
    <section id='blog' className='py-20 bg-gray-100'>
      <div className='container mx-auto text-center'>
        <h2 className='text-3xl font-bold mb-10'>Our Blog</h2>
        <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
          <div className='p-6 bg-white rounded-lg shadow-lg'>
            <img src='https://picsum.photos/id/237/200/300' alt='Blog 1' className='w-full h-48 object-cover rounded-lg mb-4' />
            <h3 className='text-xl font-bold mb-2'>The Future of AI in Business</h3>
            <p className='mb-4'>Explore emerging trends in AI and their impact on various industries.</p>
            <a href='#read-more' className='text-blue-600 hover:underline'>Read More</a>
          </div>
          <div className='p-6 bg-white rounded-lg shadow-lg'>
            <img src='https://picsum.photos/id/237/200/300' alt='Blog 2' className='w-full h-48 object-cover rounded-lg mb-4' />
            <h3 className='text-xl font-bold mb-2'>Implementing AI: Best Practices</h3>
            <p className='mb-4'>Learn how to successfully integrate AI into your business operations.</p>
            <a href='#read-more' className='text-blue-600 hover:underline'>Read More</a>
          </div>
          <div className='p-6 bg-white rounded-lg shadow-lg'>
            <img src='https://picsum.photos/id/237/200/300' alt='Blog 3' className='w-full h-48 object-cover rounded-lg mb-4' />
            <h3 className='text-xl font-bold mb-2'>AI Case Studies: Real-World Applications</h3>
            <p className='mb-4'>Get insights from businesses that have successfully implemented AI.</p>
            <a href='#read-more' className='text-blue-600 hover:underline'>Read More</a>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Blog;
