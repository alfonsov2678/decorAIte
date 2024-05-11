**decorAIte: AI for Interior Decoration**

The increasing mobility of the American population, with 25.6 million people relocating annually, underscores the challenge of transforming empty spaces into personalized homes. Current AI tools generate idealized but impractical room designs that fail to address user-specific needs. This paper presents decorAIte, a theoretical AI-based home decoration solution that leverages natural language processing, computer vision, and image composition technologies. By analyzing user-submitted room photographs and style preferences, decorAIte provides tailored, interactive design recommendations linked directly to retailers for seamless purchasing. The system integrates advanced image segmentation, object detection, and composition models to identify and position furniture from real world catalogs accurately. We use user studies to affirm the feasibility of this approach, with future enhancements aimed at expanding the product database, optimizing image composition, and improving object recognition accuracy.

**Running decorAIte**

To generate the dataset of IKEA web-scraped products, you can run:

> python3 datascraper.py

To run the web app, you can do the following to build the Docker image:

> cd backend
> docker-compose up --build

You can navigate to **http://localhost:3000** to view the app. 

If you would like to run decorAIte on a test image, do the following:
> cd backend/src/app
> conda env create -f environment.yml
> conda activate decoraite

Upload an image to your workspace and specify the path in the `INPUT_IMAGE_PATH` constant in `test.py`. Then, run:
> python3 test.py

You will find the composed images under the generated `tmp/` directory.

**Contributions**  
Sameer: Built the fine-tuned Image Composition Models using DreamCom + contributed to end-to-end pipeline
Nirvaan: Helped in setting up ControlNet + wrote evaluation script and conducted user study
Alfonso: Built the RAG similarity pipeline + helped in setting up ControlNet  
David: Built scripts for data collection and ingestion + conducted user study
