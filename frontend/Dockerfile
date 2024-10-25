# Use the official Nginx image as a base image
FROM nginx:alpine

# Copy the HTML files to the Nginx server's default location
COPY . /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
