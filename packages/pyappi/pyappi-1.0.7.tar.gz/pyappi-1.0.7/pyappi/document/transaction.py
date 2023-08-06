from pyappi.document.type import *
from pyappi.document.random_handler import *
from pyappi.document.exceptions import *
from typing import Any

import time
import os
import json


transaction_config = {
    "allow_bulk_assign": True
}
    

class Transaction:
    def __init__(self, document, tsx, key, parent=None, type="", root=None):
        self.__dict__['__document'] = document
        self.__dict__['__parent'] = parent
        self.__dict__['__root'] = root
        self.__dict__['__tsx'] = tsx
        self.__dict__['__type'] = type
        self.__dict__['__key'] = key

    def __len__(self):
        return len(self.__dict__['__document'])
    
    def __contains__(self, key):
        return key in self.__dict__['__document']
    
    def unwrap(self):
        return self.__dict__['__document']

    def __update(self, tsx, key, delta):
        self.__dict__['__document']["_cmt"] = self.__dict__['__tsx']
        self.__dict__['__parent'].__update(self.__dict__['__tsx'], self.__dict__['__key'],{key:delta})

    def __setattr__(self, __name: str, __value: Any) -> None:
        if self.__dict__['__root'].__dict__['__read_only']:
            raise ReadOnlyDocument()

        if isinstance(__value, list):
            raise "Lists are not allowed in Appi"
        
        if isinstance(self.__dict__['__document'].get(__name,None), dict):
            raise "You can't reassign a dictionary"
            
        parent_type = self.__dict__['__type']
        match parent_type:
            case "log" | "glog":
                now = int(time.time() * 1000 * 1000) 
                if not self.__dict__['__document'].get("_frame",None):
                    self.__dict__['__document']["_frame"] = now

                if not self.__dict__['__document'].get("_depth",None):
                    self.__dict__['__document']["_depth"] = 256

                if not self.__dict__['__document'].get("_size",None):
                    self.__dict__['__document']["_size"] = 32*1024

                if not self.__dict__['__document'].get("_interval",None):
                    self.__dict__['__document']["_interval"] = 60*60*24

                if not self.__dict__['__document'].get("_server_t",None):
                    self.__dict__['__document']["_server_t"] = 1

                if __name.startswith("_"):
                    self.__dict__['__document'][__name] = __value
                else:
                    time_type = self.__dict__['__document']["_server_t"]
                    interval = self.__dict__['__document']["_interval"]
                    if time_type == -1:
                        ikey = int(__name)
                        time_group = str(ikey - (ikey % interval))

                        if parent_type == "glog":
                            pass
                        else:
                            pass
                        """
                                if (current_type == "glog")
                                {
                                    if (object.Valid())
                                        tally_cb("gtally", base_key, object["~glog"]);
                                    else
                                        tally_cb("gtally", base_key, value);
                                }
                                else
                                {
                                    if (!object.Valid())
                                        return;

                                    do_ltally(base_key, 1);
                                    tally_cb("ltally", base_key, "1");
                                }"""
                        
                        """				auto log_cb = [&](auto _path, auto key, auto time_group, auto json) {
					auto log_id = std::string("_") + std::to_string(id) + "." + time_group;

					auto update = d8u::BuildJson([&](auto& root) {
						root["_perm"]([&](auto& perm) {
							perm[real_id] = "inherit";
						});

						root[_path]([&](auto& path) { 
							path[key] = json;
						});

						root["_bmt"] = -1;
					});

					auto [_result,sz] = Upsert(log_id, update, Session()/*SYSTEM*/);

					if (_result && _result != CreateOnUpsert)
					{
						auto msg = ErrorDetails[_result];
						std::cout << "TODO LOG_CB ERROR" << std::endl;
					}
				};"""
                        pass # TODO
                        #log_id = 
                        #log_cb(base_key, key, time_group, object.Json());
                    else:
                        """
                        						auto now_s = _now / (1000*1000);
							auto now = _now - frame_c;
							std::string skey = std::to_string(now);
							ordered.insert(std::stoull(skey));
							auto time_group = std::to_string(now_s - (now_s % interval));

							if (current_type == "glog")
							{
								if(object.Valid())
									tally_cb("gtally", base_key, object["~glog"]);
								else
									tally_cb("gtally", base_key, value);
							}
							else
							{
								if (!object.Valid())
									return;

								do_ltally(base_key, 1);
								tally_cb("ltally", base_key, "1");
							}

							now++;

							lookup[std::stoull(skey)] = object;
							log_cb(base_key, skey, time_group, object.Json()); // Use the base key to prevent recursion problem."""
                        pass

                    
                    """std::vector<uint64_t> dlimit(ordered.begin(), ordered.end());
					dlimit.resize((ordered.size() > depth) ? depth : ordered.size());
					
					//Cap size
					size_t csize = 0, i = 0;
					for (auto k : dlimit)
					{
						csize += lobject(k).Json().size();
						csize += robject(k).Json().size();

						if (csize > size)
							break;
						i++;
					}

					dlimit.resize(i);

					stream.KO(parent_key);

					auto [_depth,_size,_interval] = migrate_settings(lobject,robject, "log", frame_c);

					auto valmod = depth != _depth || size != _size || interval != _interval;

					for (auto k : dlimit)
					{
						auto ks = std::to_string(k);
						stream.Key(ks);

						auto robjectc = robject(ks);
						if (lookup.find(k) != lookup.end())
							robjectc = lookup[k];
						auto lobjectc = lobject(ks);

						if (robjectc.Valid())
						{
							if(_TransactedMerge(owner_cb,tally_cb,tag_cb, log_cb, update_is_master, tm, create_cb, index_cb, search_cb, file_cb, side_effects_cb, rules, t, lobjectc, robjectc, stream, log, edit_meta, is_system, path.size() ? (path + "." + (std::string)ks) : (std::string)ks, "", false, ks))
								child_mutation = true;
							global_log(lobjectc.Valid() ? "=" : "+", ks);
						}
						else
							stream.Value(lobjectc.Json());
					}

					if(valmod)
						child_mutation = true;

					stream.KV("_cmt", t.current);
					stream.KV("_vmt", (valmod) ? t.current : lobject["_vmt"]);
					stream.Close();"""
                pass
            case _:
                pass
        
        if isinstance(__value,dict) and len(__value):
            if not transaction_config["allow_bulk_assign"]:
                raise "You can't create a pre-populated dictionary"
        

        # Parent Type Handler:
        # TODO

        # Value Assignment:

        value_type = type_lookup(__name)

        match parent_type:
            case "tally" | "tly" | "ltally" | "lly" | "gly" | "gtally":
                value_type = parent_type
        
        match value_type:
            case "rng" | "random":
                self.__dict__['__document'][__name] = random_handler(__value)

            case "app" | "append":
                base = self.__dict__['__document'].get(__name,"")
                self.__dict__['__document'][__name] = base + __value
                
            case "pre" | "prepend":
                base = self.__dict__['__document'].get(__name,"")
                self.__dict__['__document'][__name] = __value + base
                
            case "flt" | "float":
                base = self.__dict__['__document'].get(__name,0)
                self.__dict__['__document'][__name] = base + __value
                
            case "cnt" | "counter":
                base = self.__dict__['__document'].get(__name,0)
                self.__dict__['__document'][__name] = base + int(__value)

            case "file" | "blocks" | "block" | "folder" | "tfile" | "tblocks" | "tblock" | "tfolder":
                file_handler()
            
            case "ltally" | "lly" | "local_tally":
                """
                    Collects all K:V tally over time by tracking and summing edits only.
                    Doesn't support deletion as it is only computed on mutation and accumulated.
                    Support logs.
                    Local tallys named "like","comments"... etc will automatically be propagated to the stats
                    {
                        something~log:{
                            25151:{files~lly:3}
                        }
                        else~ltally:{
                            files:4
                        },
                        $ltally:
                        {
                            files:7
                        }
                    }
                """

                """if (rvalid)
                {
                    if(value.size())
                        rules.Error(WontChangeTally);
                    else
                    {
                        tally_cb("ltally",base_key, rvalue);
                        add_kv(key, rvalue,true);
                        do_ltally(base_key, rvalue);
                    }
                }
                else
                    stream.KV(key, value);	"""


            case "tally" | "tly":
                """
                    Collects all current K:V spread throughout the file and sums them in a root key $tally.
                    Supports deletion as is recomputed completely every time.
                    Doesn't support logs as can't recompute the removed log items.
                    {
                        something:{
                            files~tly:3
                        }
                        else~tally:{
                            files:4
                        },
                        $tally:
                        {
                            files:7
                        }
                    }



                auto do_tally = [&](auto base_key,auto value)
				{
					int64_t v = (int64_t)value;
					auto [i, b] = t.tally.try_emplace(base_key, v);

					if (!b)
						i->second += v;
				};
                """



                """auto v = rvalid ? rvalue : value;
                do_tally(base_key, v);
                stream.KV(key, v);"""
                
            case _:
                self.__dict__['__document'][__name] = __value
            
        self.__dict__['__document']["_vmt"] = self.__dict__['__tsx']
        self.__update(self.__dict__['__tsx'],__name, self.__dict__['__document'][__name])

    def __getattr__(self, __name: str):
        __value = self.__dict__['__document'].get(__name,None)

        if not __value and self.__dict__['__root'].__dict__['__auto_nav'] and not self.__dict__['__root'].__dict__['__read_only']:
            if __name.startswith("__") and __name.endswith("__"):
                return None
            self.__dict__['__document'][__name] = {}
            __value = self.__dict__['__document'][__name]

        if isinstance(__value, dict):
            return Transaction(__value, self.__dict__['__tsx'], __name, self, type_lookup(__name,__value), self.__dict__["__root"])

        return __value
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        return self.__setattr__(__name,__value)
    
    def __getitem__(self, __name: str):
        return self.__getattr__(__name)