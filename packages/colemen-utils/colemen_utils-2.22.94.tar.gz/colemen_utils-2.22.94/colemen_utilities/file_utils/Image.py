# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel
import json
import re
from typing import Union
import os
from re import L
import time
from dataclasses import dataclass
from typing import Dict, List

from collections.abc import Iterable
import colemen_config as _config
import colemen_utilities.file_utils.File as _File


import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _f
import colemen_utilities.directory_utils as _directory
import colemen_utilities.list_utils as _arr





@dataclass
class Image(_File.File):
    name:str=None
    '''The file name of this image with the file extension'''
    name_no_ext:str=None
    '''The file name of this image without the file extension'''
    file_path:str=None
    dir_path:str=None
    extension:str=None
    synonyms:list=None
    changes_made:bool=False
    _tags:List=None
    _meta:Dict=None
    _created = time.time()
    _modified:bool = False
    _format_tags:bool = False
    _stable_diffusion_data:dict = None
    _synonyms_applied:str = None
    _original_tags_hash:str = None
    '''The sha256 hash of the tags when this image was imported'''

    def __init__(self,file:dict=None,file_path:str=None):
        self.settings = {}
        self.data = {}

        if file is None and file_path is not None:
            if _f.exists(file_path) is False:
                raise ValueError("You must provide a file dictionary or file_path")
            files = _get_meta([_f.get_data(file_path)])
            file= files[0]
        if file is not None:
            file_path = _obj.get_arg(file,["file_path","SourceFile"],None)
        super().__init__(file_path)
            # print(f"file: {file}")
        self._meta = file
        self._tags = _arr.force_list(_obj.get_arg(file,['IPTC:Keywords'],[],None))
        self._original_tags_hash = _csu.to_hash(self._tags)
        self.file_path = file['SourceFile']
        self.name = file['File:FileName']
        self.name_no_ext = _f.get_name_no_ext(file['SourceFile'])
        self.dir_path = file['File:Directory']
        self.extension = _f.get_ext(file['SourceFile'])

    @property
    def summary(self):
        '''
            Get this Image's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:08:29
            `@memberOf`: Image
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "name_no_ext":self.name_no_ext,
            "file_path":self.file_path,
            "dir_path":self.dir_path,
            "extension":self.extension,
            "tags":self._tags,
            "_meta":self._meta,
            "_created":self._created,
            "_modified":self._modified,
            "_format_tags":self._format_tags,
            "comment":self.comment,
            }
        return value

    def save(self,force=False):
        '''
            Save this image if changes have been made

            ----------

            Arguments
            -------------------------
            [`force`=False] {bool}
                If True, the image will be saved regardless of if changes have been made.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:11:33
            `memberOf`: Image
            `version`: 1.0
            `method_name`: save
            * @xxx [02-21-2023 10:12:38]: documentation for save
        '''

        if self.changes_made is True or force is True:
            from exiftool import ExifToolHelper
            with ExifToolHelper() as et:
                et.set_tags(
                    [self.file_path],
                    tags={"Keywords": self._tags}
                )
            self.clean()


    @property
    def tags_hash(self):
        '''
            Get this Image's tags_hash
            Generate a sha256 hash of the current tag list.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-22-2023 08:19:23
            `@memberOf`: Image
            `@property`: tags_hash
        '''
        value = _csu.to_hash(self._tags)
        return value

    def format_tags(self):
        if self._format_tags is True:
            return

        tags = []
        for tag in self._tags:
            tags.append(_csu.to_snake_case(tag))
        self._tags = tags
        self._format_tags = True

    def has_tag(self,tag:Union[str,list],regex:bool=False,match_all:bool=False):
        '''
            Check if this image has a matching tag or matches one of many tags.

            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                The tag or list of tags to search for.
                This can also be a comma delimited list of tags.

            [`regex`=False] {bool}
                if True, the tag will use regex for searching.

            [`match_all`=False] {bool}
                if True, the image must contain all tags provided in order to pass.

            Return {bool}
            ----------------------
            True if this image contains the search tag(s), False otherwise

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:15:17
            `memberOf`: Image
            `version`: 1.0
            `method_name`: has_tag
            * @xxx [02-21-2023 10:23:20]: documentation for has_tag
        '''
        self.format_tags()
        if "," in tag:
            tag = tag.split(",")
        tags = _arr.force_list(tag)
        has_tag = False
        for tag in tags:
            tag = _csu.strip(tag," ")
            if len(tag) == 0:
                continue
            if regex is True:
                for tg in self._tags:
                    if len(re.findall(tag,tg)) > 0:
                        has_tag = True

            else:
                snake_tag = _csu.to_snake_case(tag)
                # print(f"snake_tag:{snake_tag}")
                # print(f"self._tags:{self._tags}")
                if snake_tag in self._tags:
                    has_tag = True

            if match_all is True:
                if has_tag is False:
                    return False
        return has_tag

    def add_tag(self,tag:Union[str,list]):
        '''
            Add a new tag to this image.
            ----------

            Arguments
            -------------------------
            `tag` {str}
                The tag to add.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:24:49
            `memberOf`: Image
            `version`: 1.0
            `method_name`: add_tag
            * @xxx [02-21-2023 10:25:13]: documentation for add_tag
        '''
        self.format_tags()
        tags = _arr.force_list(tag)
        tags = [_csu.to_snake_case(x) for x in tags]
        new_tags = []
        for tag in tags:
            if tag not in self._tags:
                new_tags.append(tag)
        if len(new_tags) > 0:
            self._tags = self._tags + new_tags
            self.changes_made = True

        # new_tags = _arr.remove_duplicates(self._tags + tag)
        # if _csu.to_hash(self._tags) != _csu.to_hash(new_tags):

    def remove_tag(self,tag):
        '''
            Remove a tag from the file.
            ----------

            Arguments
            -------------------------
            `tag` {str}
                The tag to remove

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:13:08
            `memberOf`: Image
            `version`: 1.0
            `method_name`: remove_tag
            * @xxx [02-21-2023 10:13:40]: documentation for remove_tag
        '''
        self.format_tags()
        tag = _arr.force_list(tag)
        tag = [_csu.to_snake_case(x) for x in tag]
        tags = []
        for tg in self._tags:
            if tg not in tag:
                tags.append(tg)
                self.changes_made = True
        # tag = [x not in tag for x in self._tags]
        self._tags = tags

    def replace_tag(self,tag,replace,regex:bool=False,partial_match:bool=False):
        '''
            Replace a tag on this image.
            ----------

            Arguments
            -------------------------
            `tag` {str}
                The tag value to replace

            `repalce` {str}
                The value to replace the matching tag with.

            [`regex`=False] {bool}
                if True, the tag will use regex for searching.

            [`partial_match`=False] {bool}
                if True, the search tag can be found as a part of a tag.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:25:21
            `memberOf`: Image
            `version`: 1.0
            `method_name`: replace_tag
            * @xxx [02-21-2023 10:38:11]: documentation for replace_tag
        '''
        # @Mstep [] force the search tag to be a list.
        if "," in tag:
            tag = tag.split(",")
        tags = _arr.force_list(tag)

        # @Mstep [] format the already existing tags.
        self.format_tags()
        # @Mstep [] convert the replacement to snake case.
        replace = _csu.to_snake_case(replace)
        # tag = _arr.force_list(tag)
        # tag = [_csu.to_snake_case(x) for x in tag]
        new_tags = []

        tag:str
        # @Mstep [LOOP] iterate the tag search list
        for tag in tags:
            otg:str
            # @Mstep [LOOP] iterate this images tags.
            for otg in self._tags:
                # @Mstep [ELSE] if regex is True
                if regex is True:
                    # @Mstep [IF] if the regex matches.
                    if len(re.findall(tag,otg)) > 0:
                        # @Mstep [] push the replacement
                        new_tags.append(replace)
                    # @Mstep [IF] if the regex matches nothing.
                    else:
                        # @Mstep [] push the original
                        new_tags.append(otg)
                # @Mstep [ELSE] if regex is False.
                else:
                    tag = _csu.to_snake_case(tag)
                    if partial_match is False:
                        # @Mstep [IF] if the tag matches the original exactly.
                        if otg == tag:
                            # @Mstep [] push the replacement
                            new_tags.append(replace)
                        # @Mstep [IF] if the tag does not match the original exactly.
                        else:
                            # @Mstep [] push the original
                            new_tags.append(otg)
                    # @Mstep [ELSE] if partial_match is True
                    else:
                        # @Mstep [IF] if the tag is contained in the original tag.
                        if tag in otg:
                            # @Mstep [] push the replacement
                            new_tags.append(replace)
                        else:
                            # @Mstep [] push the original
                            new_tags.append(otg)


        # @Mstep [IF] if new_tags has changed
        if new_tags != self._tags:
            # @Mstep [] update the _tags property
            self._tags = new_tags
            # @Mstep [] set changes_made to True.
            self.changes_made = True

    def tag_commands(self,tag:Union[str,list]):
        self.format_tags()
        if "," in tag:
            tag = tag.split(",")
        tag = _arr.force_list(tag)
        add_tags = []
        remove_tags = []
        for tg in tag:
            if tg[0] == "-":
                tg = re.sub(r"^-","",tg)
                remove_tags.append(tg)
                # c.con.log(f"    removing tag: {tg}","red")
            else:
                add_tags.append(tg)
                # c.con.log(f"    adding tag: {tg}","green")
        add_tags = [x for x in add_tags if x not in self._tags]
        if len(add_tags) > 0:
            self.add_tag(add_tags)

        remove_tags = [x for x in remove_tags if x in self._tags]
        if len(remove_tags) > 0:
            self.remove_tag(remove_tags)

    def clean(self):
        '''
            The exif tool will create a backup copy of this image, this method will
            delete that file.

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:38:23
            `memberOf`: Image
            `version`: 1.0
            `method_name`: clean
            * @xxx [02-21-2023 10:39:03]: documentation for clean
        '''
        if _f.exists(f"{self.file_path}_original"):
            _f.delete(f"{self.file_path}_original")

    def delete(self,shred:bool=False):
        '''
            Delete this image.
            ----------

            Arguments
            -------------------------
            [`shred`=False] {bool}
                If True, this image will be shredded and securely deleted.
                This is obviously a slower process than normal deletion.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:39:13
            `memberOf`: Image
            `version`: 1.0
            `method_name`: delete
            * @xxx [02-21-2023 10:40:41]: documentation for delete
        '''
        self.format_tags()
        _f.delete(self.file_path,shred=shred)

    def apply_synonyms(self):
        '''
            Apply synonyms to this file's tags

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:41:24
            `memberOf`: Image
            `version`: 1.0
            `method_name`: apply_synonyms
            * @xxx [02-21-2023 10:41:55]: documentation for apply_synonyms
        '''
        if self._synonyms_applied != self.tags_hash:
            for syn in self.synonyms:
                if len(syn) == 2:
                    if self.has_tag(syn[0],regex=True):
                        # c.con.log(f"    Synonym Found: {syn[0]}    ","magenta invert")
                        self.tag_commands(syn[1])
            if self.is_stable_diffusion_render:
                if self.has_tag("stable_diffusion") is False:
                    self.add_tag("stable_diffusion")
            self._synonyms_applied = self.tags_hash

    def move(self,new_directory:str):
        new_path = _csu.file_path(f"{new_directory}/{self.name}")
        # print(f"move.new_path:{new_path}")
        _f.move(self.file_path,new_path)
        self.file_path = new_path
        self.dir_path = new_directory

    def copy(self,new_directory:str)->_config._image_type:
        new_path = _csu.file_path(f"{new_directory}/{self.name}")
        # print(f"copy.new_path:{new_path}")
        _f.copy(self.file_path,new_path)
        # new_image = Image(file_path=new_path)
        # new_image._tags = self.tags
        # new_image._meta = self._meta
        new_image = self.copy_meta_to_file(new_path)
        return new_image

    def copy_meta_to_file(self,file_path:str):
        '''
            Copy this files meta data to another file.
            ----------

            Arguments
            -------------------------
            `file_path` {str}
                The path to the subject file that will have its meta data overwritten.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-22-2023 13:00:41
            `memberOf`: Image
            `version`: 1.0
            `method_name`: copy_meta_to_file
            * @xxx [02-22-2023 13:01:30]: documentation for copy_meta_to_file
        '''
        # pylint: disable=protected-access
        img = Image(file_path=file_path)
        img._tags = self.tags
        img._meta = self._meta
        img.save(True)
        return img

    def convert_to_jpg(self):
        if self.extension in [".jpg"]:
            return
        jpg_path = f"{self.dir_path}/{self.name_no_ext}.jpg"
        paths = _f.convert.to_jpg(self.file_path,jpg_path)
        if len(paths) > 0:
            return self.copy_meta_to_file(paths[0])



    def rename(self,new_name:str):
        new_name = new_name.replace(self.extension,'')
        new_path = f"{self.dir_path}/{new_name}{self.extension}"
        # print(f"new_path:{new_path}")
        if _f.rename(self.file_path,new_path):
            self.file_path = new_path
            self.name_no_ext = _f.get_name_no_ext(self.file_path)
            self.name = f"{self.name_no_ext}{self.extension}"
        else:
            print(f"file_path:{self.file_path}")
            print(f"new_path:{new_path}")
            raise OSError("Failed to rename file")

    @property
    def tags(self)->Iterable[str]:
        '''
            Get this Image's tags

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 11:40:46
            `@memberOf`: Image
            `@property`: tags
        '''
        value = self._tags
        return value

    @property
    def comment(self):
        '''
            Get this Image's comment

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:11:57
            `@memberOf`: Image
            `@property`: comment
        '''

        value = _obj.get_arg(self._meta,["EXIF:UserComment"],"",str)
        return value

    @property
    def stable_diffusion_params(self)->dict:
        '''
            Get this Image's stable_diffusion_params

            If this file was generated by stable diffusion, this will parse
            the comment into its options.

            If it was not, it will return None.

            `default`:None


            `example`:
                data = {
                    "prompts":[],
                    "negative_prompt":[],
                    "steps":None,
                    "sampler":None,
                    "cfg_scale":None,
                    "seed":None,
                    "face_restoration":None,
                    "size":None,
                    "model_hash":None,
                    "model":None,
                }

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:21:07
            `@memberOf`: Image
            `@property`: stable_diffusion_params
        '''
        value = self._stable_diffusion_data
        if value is None:
            value = _parse_stable_diffusion_comment(self)
            self._stable_diffusion_data = value
        return value

    @property
    def is_stable_diffusion_render(self)->bool:
        '''
            Get this Image's is_stable_diffusion_render

            returns True if this file has stable diffusion data in its comment.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:53:46
            `@memberOf`: Image
            `@property`: is_stable_diffusion_render
        '''
        options = ["Steps","Sampler","CFG scale","Seed","Face restoration","Size","Model hash","Model"]
        options_found = False
        for op in options:
            if op in self.comment:
                options_found = True
        return options_found



def _parse_stable_diffusion_comment(img:Image):
    options = ["Steps","Sampler","CFG scale","Seed","Face restoration","Size","Model hash","Model"]
    options_found = False

    data = {
        "prompts":[],
        "negative_prompt":[],
        "steps":None,
        "sampler":None,
        "cfg_scale":None,
        "seed":None,
        "face_restoration":None,
        "size":None,
        "model_hash":None,
        "model":None,
    }

    cmt = img.comment
    for op in options:
        if op in cmt:
            options_found = True
    if options_found is False:
        return None

    cmt = cmt.replace("Negative prompt","negative_prompt")
    for op in options:
        op_snake = _csu.to_snake_case(op)
        cmt = cmt.replace(op,op_snake)
        reg = rf'(\s?{op_snake}:\s?([^\n,]*),?\s?)'
        match = re.findall(reg,cmt)
        if len(match)>0:
            match = match[0]
            # print(f"match:{match}")
            data[op_snake] = match[1]
            cmt = cmt.replace(match[0],'')

    # @Mstep [] capture the negative prompt list.
    match = re.findall(r'(\s?negative_prompt:\s?(.*))',cmt)
    if len(match)>0:
        match = match[0]
        data['negative_prompt'] = match[1].split(",")
        cmt = cmt.replace(match[0],'')
    # @Mstep [] anything that remains are positive prompts
    data['prompts'] = cmt.replace("\n","").split(",")

    return data

def apply_synonyms(images):
    # c.con.log("Applying Tag Synonyms","info invert")
    synonyms = _f.read.as_json(f"{os.getcwd()}/alice/image_organizer/synonyms.json")
    img:Image
    for img in images:
        for syn in synonyms:
            if len(syn) == 2:
                if img.has_tag(syn[0],regex=True):
                    # c.con.log(f"    Synonym Found: {syn[0]}    ","magenta invert")
                    img.tag_commands(syn[1])
        if img.is_stable_diffusion_render:
            img.add_tag("stable_diffusion")

def _get_meta(files):
    '''
        Iterate the file dictionaries provided and add the image meta data.
        ----------

        Arguments
        -------------------------
        `files` {list}
            The list of file dictionaries from colemen_utils.get_files/ get_data


        Return {list}
        ----------------------
        A list of file dictionaries with the meta data added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-21-2023 09:52:13
        `memberOf`: Image
        `version`: 1.0
        `method_name`: _get_meta
        * @xxx [02-21-2023 09:54:00]: documentation for _get_meta
    '''
    # c.con.log(f"Retrieving meta data for {len(files)} images","info")
    result_array = []
    paths = [_csu.file_path(x['file_path'],url=True) for x in files]
    import exiftool
    with exiftool.ExifToolHelper() as et:
        try:
            result_array = et.get_metadata(paths)
        except UnicodeDecodeError as e:
            # c.con.log("Failed to retrieve meta data","red invert")
            print(e)

    return result_array

# def get_images(path)->Iterable[Image]:
#     files = _f.get_files(path,extensions=['.jpg','.jpeg','.png','.jfif','.gif','.webp'])
#     synonyms = _f.read.as_json(f"{os.getcwd()}/alice/image_organizer/synonyms.json") or []
#     if len(files) == 0:
#         return []
#     files = _get_meta(files)
#     output = []
#     for file in files:
#         # print(f"file:{file}")
#         image = Image(file)
#         image.synonyms = synonyms
#         output.append(image)
#     return output




# if __name__ == "__main__":
#     imgs = get_images("C:/Users/Colemen/Desktop/TEST_FOLDER/PurgeAllButNewest")
#     for img in imgs:
#         print(f"img.tags:{img.tags}")
        # if img.is_stable_diffusion_render:
        #     for k,v in img.stable_diffusion_params.items():
        #         if k not in ["prompts","negative_prompt"]:
        #             img.add_tag(f"{k}:{v}")
        #         else:
        #             img.add_tag(v)
        # img.apply_synonyms()
        # img.save()




