# Art Gallery Frontend Application

This project is a frontend application for an art gallery, built using React, TailwindCSS, and TypeScript. It provides various pages such as Home, Shop, Drawing Details, Cart, Checkout, About Us, and Contact Us.

## Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

## Getting Started

1. Clone the repository:

```sh
$ git clone <repository-url>
```

2. Navigate to the frontend folder:

```sh
$ cd generated_src/frontend
```

3. Install the dependencies:

Using npm:

```sh
$ npm install
```

Or using yarn:

```sh
$ yarn install
```

4. Start the development server:

Using npm:

```sh
$ npm start
```

Or using yarn:

```sh
$ yarn start
```

5. Open your browser and go to `http://localhost:3000` to view the application.

## Project Structure

- `src/components`: Contains reusable React components.
- `src/pages`: Contains page components for different routes.
- `src/App.tsx`: Main application component that sets up routing.
- `src/index.tsx`: Entry point for the React application.

## Available Scripts

In the project directory, you can run:

### `npm start` or `yarn start`

Runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits. You will also see any lint errors in the console.

### `npm run build` or `yarn build`

Builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

### `npm test` or `yarn test`

Launches the test runner in interactive watch mode. To run tests once, use `CI=true npm test` or `CI=true yarn test`.

## API Integration

The application integrates with the following backend APIs:

- **Authentication API**: `/api/auth/login` and `/api/auth/register`
- **Get Drawings API**: `/api/drawings`
- **Drawing Detail API**: `/api/drawings/:id`
- **Add to Cart API**: `/api/cart`
- **Get Cart API**: `/api/cart`
- **Checkout API**: `/api/checkout`

## Deployment

To deploy the application, build the project using `npm run build` or `yarn build`. The build artifacts will be stored in the `build` folder. You can then deploy these files to a static hosting service of your choice.

## License

This project is licensed under the MIT License.
