import warnings

warnings.filterwarnings("ignore")

import copy
import io
import logging
import math
import mimetypes
import os
import random
import string
import sys
import tempfile
import lark

import click
import cv2
import numpy as np
import supervision as sv
from lark import Lark, UnexpectedCharacters, UnexpectedToken
from PIL import Image
from spellchecker import SpellChecker
from visionscript.grammar import grammar
from visionscript.usage import (USAGE, language_grammar_reference,
                                lowercase_language_grammar_reference)

spell = SpellChecker()

parser = Lark(grammar)

SUPPORTED_INFERENCE_MODELS = {
    "classify": {
        "clip": "clip",
    },
    "detect": {"yolov8": "autodistill_yolov8"},
    "segment": {"fastsam": "fastsam", "groundedsam": "autodistill_groundedsam"},
}

SUPPORTED_TRAIN_MODELS = {
    "classify": {"vit": "autodistill_vit"},
    "detect": {"yolov8": "autodistill_yolov8"},
}


def handle_unexpected_characters(e, code):
    # raise error if class doesn't exist
    line = e.line
    column = e.column

    # check if function name in grammar
    function_name = code.strip().split("\n")[line - 1].split("[")[0].strip()

    language_grammar_reference_keys = language_grammar_reference.keys()

    if function_name in language_grammar_reference_keys:
        print(f"Syntax error on line {line}, column {column}.")
        print(f"Unexpected character: {e.char!r}")
        exit(1)

    spell.known(lowercase_language_grammar_reference)
    spell.word_frequency.load_words(lowercase_language_grammar_reference)

    alternatives = spell.candidates(function_name)

    if len(alternatives) == 0:
        print(f"Function {function_name} does not exist.")
        exit(1)

    print(f"Function '{function_name}' does not exist. Did you mean one of these?")
    print("-" * 10)

    for item in list(alternatives):
        if item in lowercase_language_grammar_reference:
            print(
                list(language_grammar_reference.keys())[
                    lowercase_language_grammar_reference.index(item.lower())
                ]
            )

    exit(1)


def handle_unexpected_token(e):
    line = e.line
    column = e.column

    print(f"Syntax error on line {line}, column {column}.")
    print(f"Unexpected token: {e.token!r}")
    exit(1)


def literal_eval(string):
    return string[1:-1] if string.startswith('"') and string.endswith('"') else string


def _get_colour_name(rgb_triplet):
    import webcolors

    min_colours = {}
    for key, name in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(name)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = key

    return min_colours[min(min_colours.keys())]


aliased_functions = {
    "isita": "classify",
    "find": "detect",
    "describe": "caption",
    "getcolors": "getcolours",
}


def map_alias_to_underlying_function(alias):
    return aliased_functions.get(alias, alias)

def init_state():
    return {
        "functions": {},
        "last_loaded_image": None,
        "last_loaded_image_name": None,
        "last": None,
        "last_function_type": None,
        "last_function_args": None,
        "image_stack": [],
        "detections_stack": [],
        "history": [],
        "search_index_stack": [],
        # "current_active_model": None,
        "output": None,
    }

class VisionScript:
    def __init__(self, notebook=False):
        self.state = init_state()
        self.notebook = notebook

        self.function_calls = {
            "load": lambda x: self.load(x),
            "save": lambda x: self.save(x),
            "classify": lambda x: self.classify(x),
            "size": lambda x: self.size(x),
            "say": lambda x: self.say(x),
            "detect": lambda x: self.detect(x),
            "segment": lambda x: self.segment(x),
            "cutout": lambda x: self.cutout(x),
            "count": lambda x: self.count(x),
            "countinregion": lambda x: self.countInRegion(*x),
            "replace": lambda x: self.replace(x),
            "in": lambda x: None,
            "if": lambda x: None,
            "var": lambda x: None,
            "variable": lambda x: None,
            "comment": lambda x: None,
            "expr": lambda x: None,
            "show": lambda x: self.show(x),
            "exit": lambda x: exit(0),
            "help": lambda x: print(language_grammar_reference[x]),
            "train": lambda x: self.train(x),
            "compare": lambda x: self.show(x),
            "read": lambda x: self.read(x),
            "label": lambda x: self.label(x),
            "list": lambda x: None,
            "get": lambda x: self.get_func(x),
            "use": lambda x: self.set_state("current_active_model", x),
            "caption": lambda x: self.caption(x),
            "contains": lambda x: self.contains(x),
            "import": lambda x: self.import_(x),
            "rotate": lambda x: self.rotate(x),
            "getcolours": lambda x: self.getcolours(x),
            "get_text": lambda x: self.get_text(x),
            "greyscale": lambda x: self.greyscale(x),
            "select": lambda x: self.select(x),
            "paste": lambda x: self.paste(x),
            "pasterandom": lambda x: self.pasterandom(x),
            "resize": lambda x: self.resize(x),
            "blur": lambda x: self.blur(x),
            "make": lambda x: self.make(x),
            "args": lambda x: None,
            "setbrightness": lambda x: self.set_brightness(x),
            "search": lambda x: self.search(x),
            "similarity": lambda x: self.similarity(x),
            "readqr": lambda x: self.read_qr(x),
            "reset": lambda x: self.reset(x),
            "negate": lambda x: self.negate(x),
            "equality": lambda x: self.equality(x),
            "not_equality": lambda x: not self.equality(x),
            "input": lambda x: self.input_(x),
        }

    def input_(self, key):
        if self.state.get(literal_eval(key)) is not None:
            return self.state[literal_eval(key)]
        else:
            print(f"Input {key} does not exist.")
            exit()

    def equality(self, args):
        return args[0] == args[1]

    def negate(self, expr):
        return not expr

    def reset(self, _):
        self.state = init_state()

    def set_state(self, key, value):
        self.state[key] = value

    def make(self, args):
        print(args, "args")
        function_name = args[0].children[0].value.strip()

        function_body = lark.Tree("expr", args[1:])

        self.state["functions"][function_name] = function_body

        print(f"Function {function_name} created.")

    def load(self, filename):
        import requests
        import validators

        if isinstance(filename, np.ndarray):
            self.state["last_loaded_image"] = filename
            # save file
            import uuid
            name = str(uuid.uuid4()) + ".png"
            cv2.imwrite(name, filename)

            self.state["last_loaded_image_name"] = name

            return filename

        # if is dir, load all images
        if filename and os.path.isdir(filename):
            image_filenames = [filename + "/" + item for item in os.listdir(filename)]

            print(image_filenames)

            for image_filename in image_filenames:
                self.load(image_filename)

            return

        if filename and validators.url(filename):
            response = requests.get(filename)
            file_extension = mimetypes.guess_extension(response.headers["content-type"])

            # if not image, error
            if file_extension not in (".png", ".jpg", ".jpeg"):
                print(f"File {filename} does not represent a png, jpg, or jpeg image.")
                return None

            # 10 random characters
            filename = (
                "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(10)
                )
                + file_extension
            )

            with tempfile.NamedTemporaryFile(delete=True) as f:
                f.write(response.content)
                filename = f.name

        if self.state.get("ctx") and self.state["ctx"].get("in"):
            filename = self.state["ctx"]["active_file"]

        self.state["last_loaded_image_name"] = filename

        return np.array(Image.open(filename).convert("RGB"))[:, :, ::-1]

    def size(self, _):
        return self.state["last_loaded_image"].size

    def import_(self, args):
        # execute code from a file
        # this will update self.state for the entire script

        file_name = "".join(
            [
                letter
                for letter in args
                if letter.isalpha() or letter == "-" or letter.isdigit()
            ]
        )

        with open(file_name + ".vic", "r") as f:
            code = f.read()

        tree = parser.parse(code.strip() + "\n")

        self.parse_tree(tree)

    def cutout(self, _):
        x1, y1, x2, y2 = self.state["last"].xyxy[0]
        image = self.state["last_loaded_image"]
        cropped_image = image.crop((x1, y1, x2, y2))
        self.state["image_stack"].append(cropped_image)
        self.state["last_loaded_image"] = cropped_image

    def select(self, args):
        # if detect, select from detections
        if self.state.get("last_function_type", None) in ("detect", "segment", "classify"):
            detections = self.state["last"]

            if len(args) == 0:
                self.state["last"] = detections
            else:
                self.state["last"] = detections[args[0]]

    def paste(self, args):
        x, y = args
        self.state["last_loaded_image"].paste(self.state["image_stack"][-1], (x, y))

    def resize(self, args):
        width, height = args
        image = self.state["last_loaded_image"]
        image = image.resize((width, height))
        self.state["last_loaded_image"] = image

    def _create_index(self):
        import faiss

        index = faiss.IndexFlatL2(512)

        self.state["search_index_stack"].append(index)

        return index

    def _add_to_index(self, image):
        index = self.state["search_index_stack"][-1]

        index.add(image)

    def search(self, label):
        # embed
        import clip
        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)

        with torch.no_grad():
            # if label is a filename, load image
            if label.startswith("./") and os.path.exists(label):
                comparator = self.load(label)
            else:
                comparator = clip.tokenize([label]).to(device)

                comparator = model.encode_text(comparator)

            if len(self.state["search_index_stack"]) == 0:
                self._create_index()

                for image in self.state["image_stack"]:
                    # turn cv2 image into PIL image
                    image = Image.fromarray(image)

                    processed_image = preprocess(image).unsqueeze(0).to(device)
                    embedded_image = model.encode_image(processed_image)

                    self._add_to_index(embedded_image)

        index = self.state["search_index_stack"][-1]

        results = index.search(comparator, 5)

        image_names = []

        for result in results[1][0]:
            image_names.append(self.state["image_stack"][result])

        return image_names

    def pasterandom(self, _):
        x, y = []

        while True:
            x, y = random.randint(
                0, self.state["last_loaded_image"].size[0]
            ), random.randint(0, self.state["last_loaded_image"].size[1])

            if len(self.state["last"].xyxy) == 0:
                break

            for bbox in self.state["last"].xyxy:
                x1, y1, x2, y2 = bbox

                if x1 <= x <= x2 and y1 <= y <= y2:
                    continue

            break

        self.state["last_loaded_image"].paste(self.state["image_stack"][-1], (x, y))

    def save(self, filename):
        self.state["last_loaded_image"].save(filename)

    def count(self, args):
        if len(args) == 0:
            return len(self.state["last"].xyxy)
        else:
            return len(
                [item for item in self.state["last"].class_id if item == args[0]]
            )

    def greyscale(self, _):
        image = self.state["last_loaded_image"]
        # turn to bgr
        image = image[:, :, ::-1].copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.state["image_stack"].append(image)
        # save to test.png
        
        self.state["last_loaded_image"] = image
        self.state["output"] = image

    def get_text(self, _):
        import easyocr

        reader = easyocr.Reader(["en"])
        result = reader.readtext(self.state["last_loaded_image_name"])

        return result

    def rotate(self, args):
        image = self.state["last_loaded_image"]
        # load into cv2
        args = int(args)
        if args == 90:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif args == 180:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif args == 270:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            image = image

        self.state["last_loaded_image"] = image
        self.state["output"] = image
        self.state["image_stack"].append(image)

    def getcolours(self, k):
        if not k:
            k = 1

        from sklearn.cluster import KMeans

        image = self.state["last_loaded_image"]

        image = np.array(image)

        image = image.reshape((image.shape[0] * image.shape[1], 3))

        clt = KMeans(n_clusters=k)

        clt.fit(image)

        # map to human readable colour
        centers = clt.cluster_centers_

        human_readable_colours = []

        for center in centers:
            try:
                human_readable_colours.append(
                    _get_colour_name((int(center[0]), int(center[1]), int(center[2])))
                )
            except ValueError as e:
                print(e)
                continue

        self.state["last"] = human_readable_colours[:k]

        return human_readable_colours[:k]

    def detect(self, classes):
        logging.disable(logging.CRITICAL)

        if self.state.get("current_active_model") and self.state["current_active_model"].lower() == "groundingdino":
            from autodistill_grounding_dino import GroundingDINO
            from autodistill.detection import CaptionOntology

            mapped_items = {item: item for item in classes}

            base_model = GroundingDINO(CaptionOntology(mapped_items))

            inference_results = base_model.predict(self.state["last_loaded_image"])
        else:
            from ultralytics import YOLO

            # model name should be only letters and - and numbers

            model_name = self.state.get("current_active_model", "yolov8n")

            model_name = "".join(
                [
                    letter
                    for letter in model_name
                    if letter.isalpha() or letter == "-" or letter.isdigit()
                ]
            )

            if self.state.get("model") and self.state["current_active_model"].lower() == "yolo":
                model = model
            else:
                model = YOLO(model_name + ".pt")

            inference_results = model(self.state["last_loaded_image"])[0]

            logging.disable(logging.NOTSET)

            # Inference
            results = sv.Detections.from_yolov8(inference_results)

        inference_classes = inference_results.names

        if len(classes) == 0:
            classes = inference_classes

        classes = [key for key, item in inference_classes.items() if item in classes]

        results = results[np.isin(results.class_id, classes)]

        self.state["detections_stack"].append(results)

        return results

    def classify(self, labels):
        image = self.state["last"]

        if self.state.get("model") and self.state["model"].__class__.__name__ == "ViT":
            model = self.state["model"]

            results = model.predict(image).get_top_k(1)

            if len(results.class_id) == 0:
                return sv.Classifications.empty()

            return results.class_id[0]
        elif (
            self.state.get("model")
            and self.state["model"].__class__.__name__ == "YOLOv8"
        ):
            model = self.state["model"]

            results = model.predict(image)

            return results

        if "clip" not in sys.modules:
            import clip
            import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("ViT-B/32", device=device)

        image = (
            preprocess(Image.open(self.state["last_loaded_image_name"]))
            .unsqueeze(0)
            .to(device)
        )
        text = clip.tokenize(labels).to(device)

        with torch.no_grad():
            logits_per_image, _ = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            # get idx of the most likely label class
            label_idx = probs.argmax()

            label_name = labels[label_idx]

        self.state["output"] = label_name

        return label_name

    def segment(self, text_prompt):
        # check for model
        from fastsam import FastSAM, FastSAMPrompt

        logging.disable(logging.CRITICAL)
        model = FastSAM("./weights/FastSAM.pt")

        DEVICE = "cpu"
        everything_results = model(
            self.state["last_loaded_image_name"],
            device=DEVICE,
            retina_masks=True,
            imgsz=1024,
            conf=0.4,
            iou=0.9,
        )
        prompt_process = FastSAMPrompt(
            self.state["last_loaded_image_name"], everything_results, device=DEVICE
        )

        # text prompt
        ann = prompt_process.text_prompt(text=text_prompt)
        logging.disable(logging.NOTSET)

        results = []
        class_ids = []

        for mask in ann:
            results.append(
                sv.Detections(
                    mask=np.array([mask]),
                    xyxy=sv.mask_to_xyxy(np.array([mask])),
                    class_id=np.array([0]),
                    confidence=np.array([1]),
                )
            )
            class_ids.append(0)

        return sv.Detections(
            mask=np.array([item.mask[0] for item in results]),
            xyxy=np.array([item.xyxy[0] for item in results]),
            class_id=np.array(class_ids),
            confidence=np.array([1]),
        )

    def countInRegion(self, x1, y1, x2, y2):
        detections = self.state["last"]

        xyxy = detections.xyxy

        counter = 0

        for i in range(len(xyxy)):
            x1_, y1_, x2_, y2_ = xyxy[i]

            if x1_ >= x1 and y1_ >= y1 and x2_ <= x2 and y2_ <= y2:
                counter += 1

        return counter

    def read(self, _):
        if self.state.get("last_function_type", None) in ("detect", "segment"):
            last_args = self.state["last_function_args"]
            statement = "".join(
                [
                    f"{last_args[0]} {self.state['last'].confidence[i]:.2f} {self.state['last'].xyxy[i]}\n"
                    for i in range(len(self.state["last"].xyxy))
                ]
            )

            return statement

        return self.state["last"]

    def say(self, statement):
        # if list, say each item
        # if last item is an image, execute show
        if isinstance(self.state["last"], np.ndarray):
            self.show(None)
            return

        if isinstance(self.state["last"], list):
            self.state["output"] = ""
            for item in self.state["last"]:
                print(item)
                # if list or tuple, join
                if isinstance(item, (list, tuple)):
                    item = ", ".join([str(i) for i in item])

                self.state["output"] += item + "\n"

            return

        if isinstance(statement, int):
            statement = str(statement)

        if statement and isinstance(statement, str):
            print(statement.strip())
            return

        if self.state.get("last_function_type", None) in ("detect", "segment"):
            last_args = self.state["last_function_args"]
            statement = "".join(
                [
                    f"{last_args} {self.state['last'].confidence[i]:.2f} {self.state['last'].xyxy[i]}\n"
                    for i in range(len(self.state["last"].xyxy))
                ]
            )
        elif isinstance(self.state["last"], list):
            statement = ", ".join([str(item) for item in self.state["last"]])
        else:
            statement = self.state["last"]

        if statement:
            print(statement.strip())

        self.state["output"] = statement

    def blur(self, args):
        image = self.state["last_loaded_image"]

        image = cv2.blur(image, (args[0], args[0]))

        self.state["last_loaded_image"] = image

    def replace(self, color):
        detections = self.state["last"]

        xyxy = detections.xyxy

        if color is not None:
            import webcolors

            try:
                color_to_rgb = webcolors.name_to_rgb(color)
            except ValueError:
                print(f"Color {color} does not exist.")
                return

            random_img = np.ones(
                (int(xyxy[0][2] - xyxy[0][0]), int(xyxy[0][3] - xyxy[0][1]), 3),
                dtype=np.uint8,
            )

            random_img[:, :] = color_to_rgb

            random_img = Image.fromarray(random_img)
        else:
            random_img = np.zeros(
                (int(xyxy[0][2] - xyxy[0][0]), int(xyxy[0][3] - xyxy[0][1]), 3),
                dtype=np.uint8,
            )

            random_img = Image.fromarray(random_img)

        # paste image
        self.state["last_loaded_image"].paste(
            random_img, (int(xyxy[0][0]), int(xyxy[0][1]))
        )

    def label(self, args):
        folder = args[0]
        model = args[1]
        items = args[2]

        if (
            "Detect" in self.state["history"]
            or self.state["current_active_model"] == "groundedsam"
        ):
            from autodistill.detection import CaptionOntology
            from autodistill_grounded_sam import GroundedSAM

            mapped_items = {item: item for item in items}

            base_model = GroundedSAM(CaptionOntology(mapped_items))
        else:
            print("Please specify a model with which to label images.")
            return

        base_model.label(folder)

    def caption(self, _):
        from transformers import BlipForConditionalGeneration, BlipProcessor

        processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        inputs = processor(self.state["last_loaded_image"], return_tensors="pt")

        out = model.generate(**inputs)

        self.state["last"] = processor.decode(out[0], skip_special_tokens=True)

        return processor.decode(out[0], skip_special_tokens=True)

    def train(self, args):
        folder = args[0]
        model = args[1]
        # if Detect or Classify run, train
        if "Detect" in self.state["history"] or model == "yolov8":
            if "autodistill_yolov8" not in sys.modules:
                from autodistill_yolov8 import YOLOv8

            base_model = YOLOv8("yolov8n.pt")

            model = base_model.train(os.path.join(folder, "data.yaml"), epochs=10)

        elif "Classify" in self.state["history"] or model == "vit":
            if "autodistill_vit" not in sys.modules:
                import autodistill_vit as ViT

            base_model = ViT("ViT-B/32")

            model = base_model.train(folder, "ViT-B/32")
        else:
            print("No training needed.")
            return

        self.state["model"] = model

    def show(self, _):
        # get most recent Detect or Segment
        most_recent_detect_or_segment = None

        for i in range(len(self.state["history"]) - 1, -1, -1):
            if self.state["history"][i] in ("detect", "segment"):
                most_recent_detect_or_segment = self.state["history"][i]
                break

        if most_recent_detect_or_segment == "detect":
            annotator = sv.BoxAnnotator()
        elif most_recent_detect_or_segment == "segment":
            annotator = sv.MaskAnnotator()
        else:
            annotator = None

        if self.state.get("last_loaded_image_name") is None or not os.path.exists(
            self.state["last_loaded_image_name"]
        ):
            print("Image does not exist.")
            return

        if self.state.get("history", [])[-2] == "search":
            images = []

            grid_size = math.gcd(len(self.state["last"]), len(self.state["last"]))

            if len(self.state["last"]) == len(self.state["detections_stack"]):
                for image, detections in zip(
                    self.state["last"], self.state["detections_stack"]
                ):
                    if annotator and detections:
                        image = annotator.annotate(np.array(image), detections)
                    else:
                        image = np.array(image)

                    images.append(image)
            else:
                for image in self.state["last"]:
                    images.append(np.array(image))

            sv.plot_images_grid(
                images=np.array(images), grid_size=(grid_size, grid_size), size=(12, 12)
            )

            return

        elif self.state.get("history", [])[-1] == "compare":
            images = []

            grid_size = math.gcd(
                len(self.state["image_stack"]), len(self.state["image_stack"])
            )

            for image, detections in zip(
                self.state["image_stack"], self.state["detections_stack"]
            ):
                if annotator and detections:
                    image = annotator.annotate(np.array(image), detections)
                else:
                    image = np.array(image)

                images.append(image)

            sv.plot_images_grid(
                images=np.array(images), grid_size=(grid_size, grid_size), size=(12, 12)
            )

            return

        if annotator:
            image = annotator.annotate(
                cv2.imread(self.state["last_loaded_image_name"]),
                self.state["detections_stack"][-1],
            )
        elif self.state.get("last_loaded_image") is not None:
            image = self.state["last_loaded_image"]
        else:
            image = cv2.imread(self.state["last_loaded_image_name"])

        if self.notebook:
            buffer = io.BytesIO()
            import base64

            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            # show image
            fig = plt.figure(figsize=(8, 8))
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            fig.savefig(buffer, format="png")
            buffer.seek(0)

            image = Image.open(buffer)

            self.state["output"] = {
                "image": base64.b64encode(buffer.getvalue()).decode("utf-8")
            }

            return

        sv.plot_image(image, (8, 8))

    def get_func(self, x):
        self.state["last"] = self.state["last"][x]

    def similarity(self, n):
        # get similarity of last N images
        if not n:
            n = 2

        if len(self.state["image_stack"]) < 2 or len(self.state["image_stack"]) < n:
            print("Not enough images to compare.")
            return

        import clip
        import torch

        device = "cuda" if torch.cuda.is_available() else "cpu"

        model, preprocess = clip.load("ViT-B/32", device=device)

        images = []

        for image in self.state["image_stack"][-n:]:
            image = preprocess(Image.fromarray(image)).unsqueeze(0).to(device)
            images.append(image)

        embeddings = []

        with torch.no_grad():
            for image in images:
                image = model.encode_image(image)

                embeddings.append(image)

        # get similarity
        similarity = torch.cosine_similarity(embeddings[0], embeddings[1])

        self.state["last"] = similarity

    def read_qr(self, _):
        import pyzbar.pyzbar as pyzbar

        image = self.state["last_loaded_image"]

        decoded_objects = pyzbar.decode(image)

        return decoded_objects

    def set_brightness(self, brightness):
        # brightness is between -100 and 100
        image = self.state["last_loaded_image"]

        # use cv2
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # add brightness
        lim = 255 - brightness

        v[v > lim] = 255
        v[v <= lim] += brightness

        final_hsv = cv2.merge((h, s, v))

        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        self.state["last_loaded_image"] = image

    def contains(self, statement):
        if isinstance(self.state["last"], str):
            return statement in self.state["last"]
        else:
            return False

    def parse_tree(self, tree):
        if not hasattr(tree, "children"):
            if hasattr(tree, "value") and tree.value.isdigit():
                return int(tree.value)
            elif isinstance(tree, str):
                return literal_eval(tree)
        
        if hasattr(tree, "children") and tree.data == "input":
            return self.input_(tree.children[0].value)

        for node in tree.children:
            if node == "True":
                return True
            elif node == "False":
                return False
            # if equality, check if equal
            elif hasattr(node, "data") and node.data == "equality":
                return self.parse_tree(node.children[0]) == self.parse_tree(
                    node.children[1]
                )
            elif node is True or node is False:
                return node
            elif hasattr(node, "data") and node.data == "list":
                node = node
            elif (hasattr(node, "type") and node.type == "INT") or isinstance(
                node, int
            ):
                return int(node.value)
            elif not hasattr(node, "children") or len(node.children) == 0:
                node = node
            elif self.state.get("ctx") and (
                self.state["ctx"].get("in") or self.state["ctx"].get("if")
            ):
                node = node
            # if string
            elif len(node.children) == 1 and hasattr(node.children[0], "value"):
                return node.children[0].value
            else:
                node = node.children[0]

            if not hasattr(node, "data"):
                continue

            token = node.data

            if token.value in aliased_functions:
                token.value = map_alias_to_underlying_function(token.value)
            
            if token.type == "equality":
                return self.parse_tree(node.children[0]) == self.parse_tree(
                    node.children[1]
                )

            if token == "comment":
                continue

            if token == "expr":
                self.parse_tree(node)
                continue

            if token.type == "BOOL":
                return node.children[0].value == "True"

            if token == "list":
                results = []

                for item in node.children:
                    results.append(self.parse_tree(item))

                return results

            if token == "var":
                self.state[node.children[0].children[0].value] = self.parse_tree(
                    node.children[1]
                )
                self.state["last"] = self.state[node.children[0].children[0].value]
                continue

            if token.value == "if":
                # copy self.state
                last_state_before_if = copy.deepcopy(self.state)["last"]

                self.state["ctx"] = {
                    "if": True,
                }

                # if equality, check if equal

                statement = node.children[0]

                statement = self.parse_tree(statement)

                print(statement, "xxx")

                if statement is None:
                    continue

                if statement is False:
                    return

                self.state["last"] = last_state_before_if

            if token.value == "make":
                self.make(node.children)
                continue

            if token.value == None:
                continue

            if token.value == "run":
                function_name = node.children[0].value

                print(f"Running {function_name}...")

                if function_name not in self.state["functions"]:
                    print(f"Function {function_name} does not exist.")
                    exit(1)

                function_args = self.state["functions"][function_name]

                for item in function_args:
                    self.parse_tree(item)

                continue

            if token.value == "literal":
                func = self.state["functions"][node.children[0].value]
            else:
                func = self.function_calls[token.value]

            if token.value == "negate" or token.value == "input":
                return func(self.parse_tree(node.children[0]))

            if token.value == "get":
                continue

            self.state["history"].append(token.value)

            if token.value == "say":
                value = self.state["last"]
                func(value)
                continue
            elif token.value == "contains":
                return func(literal_eval(node.children[0]))
            else:
                # convert children to strings
                for item in node.children:
                    if hasattr(item, "value"):
                        if item.value.startswith('"') and item.value.endswith('"'):
                            item.value = literal_eval(item.value)
                        elif item.type in ("EOL", "INDENT", "DEDENT"):
                            continue
                        elif item.type == "STRING":
                            item.value = literal_eval(item.value)
                        elif item.type == "INT":
                            item.value = int(item.value)

            if token.value == "in":
                self.state["ctx"] = {
                    "in": os.listdir(node.children[0].value),
                }

                for file_name in self.state["ctx"]["in"]:
                    self.state["ctx"]["active_file"] = os.path.join(
                        literal_eval(node.children[0]), file_name
                    )
                    # ignore first 2, then do rest
                    context = node.children[3:]

                    for item in context:
                        self.parse_tree(item)

                del self.state["ctx"]

                continue

            if len(node.children) == 1:
                if hasattr(node.children[0], "value"):
                    value = node.children[0].value
                else:
                    value = self.parse_tree(node.children[0])
            elif all([hasattr(item, "value") for item in node.children]):
                value = [item.value for item in node.children]
            else:
                value = [self.parse_tree(item) for item in node.children]

            if token.value == "literal":
                result = self.parse_tree(self.state["functions"][value])
            else:
                result = func(value)

            if result is not None:
                self.state["last"] = result
                self.state["output"] = result

            self.state["last_function_type"] = token.value
            self.state["last_function_args"] = [value]

            if token.value == "load":
                self.state["image_stack"].append(result)
                self.state["last_loaded_image"] = result


def activate_console(parser):
    print("Welcome to VisionScript!")
    print("Type 'Exit[]' to exit.")
    print("Read the docs at https://visionscript.org/docs")
    print("For help, type 'Help[FunctionName]'.")
    print("-" * 20)
    session = VisionScript()

    while True:
        code = input(">>> ")

        try:
            tree = parser.parse(code.lstrip())
        except UnexpectedCharacters as e:
            handle_unexpected_characters(e, code.lstrip())
        except UnexpectedToken as e:
            handle_unexpected_token(e)

        session.parse_tree(tree)


@click.command()
@click.option("--validate", default=False, help="")
@click.option("--ref", default=False, help="Name of the file")
@click.option("--debug", default=False, help="To debug")
@click.option("--file", default=None, help="Name of the file")
@click.option("--repl", default=None, help="To enter to vscript console")
@click.option("--notebook/--no-notebook", help="To enter to vscript console")
def main(validate, ref, debug, file, repl, notebook) -> None:
    if validate:
        print("Script is a valid VisionScript program.")
        exit(0)

    if ref:
        print(USAGE.strip())

    if notebook:
        print("Starting notebook...")
        import webbrowser
        from notebook import app
        import uuid

        # webbrowser.open("http://localhost:5000/notebook?" + str(uuid.uuid4()))

        app.run(debug=True)

    if file is not None:
        with open(file, "r") as f:
            code = f.read() + "\n"

        tree = parser.parse(code.lstrip())

        if debug:
            print(tree.pretty())
            exit()

        session = VisionScript()

        # args = {"image": "./indieweb.jpg"}

        # # merge state and args
        # session.state = {**session.state, **args}

        session.parse_tree(tree)

    if repl == "console":
        activate_console(parser)


if __name__ == "__main__":
    main()
