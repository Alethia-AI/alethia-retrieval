# `privocia-py`

Python client for [Privocia](https://privocia.re)

- Documentation: [docs.privocia.re](https://docs.privocia.re/reference/python/introduction)
- Usage:
  - [Forage](https://privocia-forage-v1.vercel.app/)

## Set up a Local Development Environment

### Clone the Repository

```bash
git clone https://github.com/Privocia/privocia-python.git
cd privocia-python
```

### Create and Activate a Virtual Environment

Using venv (Python 3 built-in):

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use .\env\Scripts\activate
```

### PyPi installation

Install the package (for > Python 3.7):

```bash
# with pip
pip install privocia
```

**Note**: Package is not yet available on PyPi. This is a placeholder for when it is available.

### Local installation

You can also install locally after cloning this repo. Install Development mode with `pip install -e`, which makes it so when you edit the source code the changes will be reflected in your python module.

## Basic Usage

```python
from privocia import PrivociaClient
privocia = PrivociaClient(api_key="YOUR_API_KEY")

# For adding url to archive:
privocia.add_url_to_archive(url="https://www.example.com")
# For adding text to archive:
privocia.add_text_to_archive(text="This is a sample text.")
# For adding image to archive:
privocia.add_image_to_archive(image_path="path/to/image.jpg")

# For searching locally:
privocia.search_local(query="sample query")
# For searching the web:
privocia.search_web(query="sample query")
```

## API Methods

### Client
The Client class is your gateway to using the Privocia API. Start by creating an instance with your API key.

### Methods
#### Search Methods
- `search_local(query, **kwargs)`: Performs a search using the specified query on the local archive.
- `search_web(query, **kwargs)`: Performs a search using the specified query on the web archive.
#### Archive Methods
- `add_url_to_archive(url, **kwargs)`: Adds the specified URL to the archive.
- `add_text_to_archive(text, **kwargs)`: Adds the specified text to the archive.
- `add_image_to_archive(image_path, **kwargs)`: Adds the specified image to the archive.
<!---
- `get_archive(archive_id, **kwargs)`: Retrieves the specified archive.
-->
- `get_archives(**kwargs)`: Retrieves all archives.
- `clear_archive(archive_id, **kwargs)`: Clears the specified archive.

### Keyword Arguments (Search)
- `query` (str): The search query.
- `query_order` (int): The order of the query. Default is 0.
- `max_results` (int): The maximum number of results to return. Default is 5.
- `archive_id` (str): The identifier for the archive. Default is None.
- `namespace_id` (str): The identifier for the namespace. Default is None.
- `index_id` (str): The identifier for the index. Default is None.
- `use_cache` (bool): Whether to use the cache. Default is True.

Both search methods (`search_local` and `search_web`) call the `_search` method with the appropriate `type_` keyword argument set to either `local` or `web`.

### Keyword Arguments (Archive)
- `url_` (str): URL of the web content to add. Default is None. when adding text.
- `text_` (str): Text content to add. Default is None. when adding url or images.
- `image_path` (str): The path to the image to add to the archive.
- `type_` (str): Type of content to add or search (e.g., web, images, text).
- `size` (str): Size of the content. Default is None.
- `vec_dim` (str): Dimension of vector representation. Default is None.
- `vec_modality`: (str): Modality of vector representation (e.g., text, image). Default is None, and set to image -> text for images.
- `index_id` (str): Identifier for the index. Default is None.
- `namespace_id` (str): Identifier for the namespace. Default is None.
- `archive_id` (str): Identifier for the archive. Default is None.

The archive methods (`add_url_to_archive`, `add_text_to_archive`, and `add_image_to_archive`) call the `_add_to_archives` method with the appropriate `type_` keyword argument set to either `url`, `text`, or `image`.

## Roadmap

- [ ] Wrap [privocia-rest](https://github.com/Privocia-Org/privocia-rest)
  - [x] Add usage functionalities.
  - [ ] Test and document common flows.
  - [ ] Add option to get/clear specific archive.
  - [ ] Add proper error handling.
  - [ ] Add proper logging.
- [ ] Release Python package on PyPi.
  - [ ] Add proper versioning.
  - [ ] Add proper documentation.
  - [ ] Add proper tests.
- [ ] Add examples in `examples` directory.
  - [ ] Add example for forage.
- [ ] Add support for [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)
  - [ ] Add docs for creating and initializing virtual environment.
  - [ ] Test and document common flows.

### Overall Tasks

- [ ] Populate README.md as developement goes along.
- [ ] Add support for running tests.
- [ ] Add section, infra, and protocol for contributing.
- [ ] Add corresponding badges.


## Badges

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?label=license)](https://opensource.org/licenses/MIT)
