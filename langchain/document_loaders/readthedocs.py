"""Loader that loads ReadTheDocs documentation directory dump."""
from pathlib import Path
from typing import Any, List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class ReadTheDocsLoader(BaseLoader):
    """Loader that loads ReadTheDocs documentation directory dump."""

    def __init__(
        self,
        path: str,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **kwargs: Optional[Any]
    ):
        """Initialize path."""
        try:
            from bs4 import BeautifulSoup

        except ImportError:
            raise ValueError(
                "Could not import python packages. "
                "Please install it with `pip install beautifulsoup4`. "
            )

        try:
            _ = BeautifulSoup(
                "<html><body>Parser builder library test.</body></html>", **kwargs
            )
        except Exception as e:
            raise ValueError("Parsing kwargs do not appear valid") from e

        self.file_path = path
        self.encoding = encoding
        self.errors = errors
        self.bs_kwargs = kwargs

    def load(self) -> List[Document]:
        """Load documents."""
        from bs4 import BeautifulSoup
        from bs4.element import Comment
        print("readthedocs - load func")

        # def _clean_data(data: str) -> str:
        #     soup_kwargs = self.bs_kwargs or {'parser': 'html.parser'}
        #     soup = BeautifulSoup(data, **soup_kwargs)
        #     # soup = BeautifulSoup(data, **self.bs_kwargs )
        #     text = soup.findAll(text=True)
        #     print(text)
        #     if len(text) != 0:
        #         text = text[0].get_text()
        #     else:
        #         text = ""
        #     print(text)
        #     return "\n".join([t for t in text.split("\n") if t])
        
        # //https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True
        
        def _clean_data(data: str) -> str:
            print('_clean_data')
            soup = BeautifulSoup(data, **self.bs_kwargs)
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts) 
            text = u" ".join(t.strip() for t in visible_texts)
            print(text)
            return text
        
        
        docs = []
        print("self.file_path: "+ self.file_path)
        for p in Path(self.file_path).rglob("*"):
            if p.is_dir():
                continue
            with open(p, encoding=self.encoding, errors=self.errors) as f:
                text = _clean_data(f.read())
            metadata = {"source": str(p)}
            docs.append(Document(page_content=text, metadata=metadata))
        return docs
