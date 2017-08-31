# -*- coding: utf-8 -*-

import os
from pathlib import Path
import json


class NotesExport:

    def __init__(self, src=False):
        self.cwd = Path(os.getcwd())
        # change target folder here:
        self.target_path = "{0}/xyayz/src/data/notes.json".format(self.cwd.parent)
        self.notes_dict = {"notes": []}
        self.checkup = []
        if src:
            self.root, self.file_list = self.get_filelist()
        else:
            default_src = "{0}/somenotes".format(self.cwd)
            self.root, self.file_list = self.get_filelist(default_src)

    def get_filelist(self, src):
        """Returns the root folder and a list of files from a given source folder (arg)."""
        for root, dirs, files in os.walk(src):
            # some filenames contain problematic chars, that's the best way I managed to come up with
            # trying to print() directly throws an Error, encoding with utf-8 creates bytes objects
            # this here works, although it simply removes those characters.
            file_list = [f.encode('ascii', 'ignore').decode('utf-8') for f in files]
            root_path = root
        return root_path, file_list

    def strip_surplus(self, file_name):
        """Removes the ".html suffix from the note's file name."""
        title = file_name[:-5]
        return title

    def create_note_dict(self):
        """
        Gets title and text body from each note and adds it to a list in the notes_dict.

        @:param
            self.file_list (list of str): all file names
            self.root (str): the directory name that contains the files
            self.checkup (list): empty list
        @:return (writes directly into the class instance's instance variables)
            self.notes_dict (dict holding a list of dicts): all notes, prepared for JSON
            self.checkup (list of str): filenames of files that didn't work out
        """
        for fl in self.file_list:
            file_path = "{0}/{1}".format(self.root, fl)
            # some don't want to work, due to the char issue mentioned above
            # creates paths that don't exist like that
            # and some others have ascii-decoding problems (uncomment Exception print() for details)
            try:
                with open(file_path, "r") as f:
                    text = f.read()
                    title = self.strip_surplus(fl)
                    note = {
                        "title": title,
                        "body": text
                    }
                    self.notes_dict["notes"].append(note)
            except Exception as e:
                #print("{0} <-- needs checking ({1})\n".format(fl, e))
                self.checkup.append(fl)
        return

    def cast_json(self):
        """Wrapper function that calls the others and writes the notes in JSON to the target path."""
        self.create_note_dict()
        with open(self.target_path, "w") as f:
            json.dump(self.notes_dict, f)


if __name__ == "__main__":
    ne = NotesExport()
    ne.cast_json()
