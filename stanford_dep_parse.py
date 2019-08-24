import stanfordnlp
import stanfordnlp
stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
# IMPORTANT: The above line prompts you before downloading, which doesn't work well in a Jupyter notebook.
# To avoid a prompt when using notebooks, instead use: >>> stanfordnlp.download('en', force=True)
nlp = stanfordnlp.Pipeline() # This sets up a default neural pipeline in English

doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
