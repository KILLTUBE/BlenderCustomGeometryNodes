/*
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * The Original Code is Copyright (C) 2001-2002 by NaN Holding BV.
 * All rights reserved.
 */

/** \file
 * \ingroup DNA
 * \brief blenloader genfile private function prototypes
 */

#pragma once

#include "dna_utils.h"

struct SDNA;

#ifdef __cplusplus
extern "C" {
#endif

/**
 * DNAstr contains the prebuilt SDNA structure defining the layouts of the types
 * used by this version of Blender. It is defined in a file dna.c, which is
 * generated by the makesdna program during the build process (see makesdna.c).
 */
extern const unsigned char DNAstr[];
/** Length of DNAstr. */
extern const int DNAlen;

/**
 * Primitive (non-struct, non-pointer/function/array) types,
 * \warning Don't change these values!
 * Currently changes here here will work on native endianness,
 * however #DNA_struct_switch_endian currently checks these
 * hard-coded values against those from old files.
 */
typedef enum eSDNA_Type {
  SDNA_TYPE_CHAR = 0,
  SDNA_TYPE_UCHAR = 1,
  SDNA_TYPE_SHORT = 2,
  SDNA_TYPE_USHORT = 3,
  SDNA_TYPE_INT = 4,
  /* SDNA_TYPE_LONG     = 5, */ /* deprecated (use as int) */
  /* SDNA_TYPE_ULONG    = 6, */ /* deprecated (use as int) */
  SDNA_TYPE_FLOAT = 7,
  SDNA_TYPE_DOUBLE = 8,
/* ,SDNA_TYPE_VOID = 9 */
/* define so switch statements don't complain */
#define SDNA_TYPE_VOID 9
  SDNA_TYPE_INT64 = 10,
  SDNA_TYPE_UINT64 = 11,
  SDNA_TYPE_INT8 = 12,
} eSDNA_Type;

/**
 * For use with #DNA_struct_reconstruct & #DNA_struct_get_compareflags
 */
enum eSDNA_StructCompare {
  /* Struct has disappeared
   * (values of this struct type will not be loaded by the current Blender) */
  SDNA_CMP_REMOVED = 0,
  /* Struct is the same
   * (can be loaded with straight memory copy after any necessary endian conversion) */
  SDNA_CMP_EQUAL = 1,
  /* Struct is different in some way
   * (needs to be copied/converted field by field) */
  SDNA_CMP_NOT_EQUAL = 2,
  /* This is only used temporarily by #DNA_struct_get_compareflags. */
  SDNA_CMP_UNKNOWN = 3,
};

struct SDNA *DNA_sdna_from_data(const void *data,
                                const int data_len,
                                bool do_endian_swap,
                                bool data_alloc,
                                const char **r_error_message);
void DNA_sdna_free(struct SDNA *sdna);

/* Access for current Blender versions SDNA*/
void DNA_sdna_current_init(void);
/* borrowed reference */
const struct SDNA *DNA_sdna_current_get(void);
void DNA_sdna_current_free(void);

struct DNA_ReconstructInfo;
struct DNA_ReconstructInfo *DNA_reconstruct_info_create(const struct SDNA *oldsdna,
                                                        const struct SDNA *newsdna,
                                                        const char *compare_flags);
void DNA_reconstruct_info_free(struct DNA_ReconstructInfo *reconstruct_info);

int DNA_struct_find_nr_ex(const struct SDNA *sdna, const char *str, unsigned int *index_last);
int DNA_struct_find_nr(const struct SDNA *sdna, const char *str);
void DNA_struct_switch_endian(const struct SDNA *sdna, int struct_nr, char *data);
const char *DNA_struct_get_compareflags(const struct SDNA *sdna, const struct SDNA *newsdna);
void *DNA_struct_reconstruct(const struct DNA_ReconstructInfo *reconstruct_info,
                             int old_struct_nr,
                             int blocks,
                             const void *old_blocks);

int DNA_elem_offset(struct SDNA *sdna, const char *stype, const char *vartype, const char *name);

int DNA_elem_size_nr(const struct SDNA *sdna, short type, short name);

bool DNA_struct_find(const struct SDNA *sdna, const char *stype);
bool DNA_struct_elem_find(const struct SDNA *sdna,
                          const char *stype,
                          const char *vartype,
                          const char *name);

int DNA_elem_type_size(const eSDNA_Type elem_nr);

bool DNA_sdna_patch_struct(struct SDNA *sdna,
                           const char *struct_name_old,
                           const char *struct_name_new);
bool DNA_sdna_patch_struct_member(struct SDNA *sdna,
                                  const char *struct_name,
                                  const char *elem_old,
                                  const char *elem_new);

void DNA_sdna_alias_data_ensure(struct SDNA *sdna);

/* Alias lookups (using runtime struct member names). */
int DNA_struct_alias_find_nr_ex(const struct SDNA *sdna,
                                const char *str,
                                unsigned int *index_last);
int DNA_struct_alias_find_nr(const struct SDNA *sdna, const char *str);
bool DNA_struct_alias_elem_find(const struct SDNA *sdna,
                                const char *stype,
                                const char *vartype,
                                const char *name);
void DNA_sdna_alias_data_ensure_structs_map(struct SDNA *sdna);

#ifdef __cplusplus
}
#endif
