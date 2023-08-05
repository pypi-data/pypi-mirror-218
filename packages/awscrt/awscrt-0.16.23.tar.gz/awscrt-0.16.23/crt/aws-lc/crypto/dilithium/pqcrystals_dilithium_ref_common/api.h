#ifndef API_DILITHIUM_H
#define API_DILITHIUM_H

#include <stddef.h>
#include <stdint.h>
#include "openssl/base.h"

#define pqcrystals_dilithium2_PUBLICKEYBYTES 1312
#define pqcrystals_dilithium2_SECRETKEYBYTES 2528
#define pqcrystals_dilithium2_BYTES 2420

#define pqcrystals_dilithium2_ref_PUBLICKEYBYTES pqcrystals_dilithium2_PUBLICKEYBYTES
#define pqcrystals_dilithium2_ref_SECRETKEYBYTES pqcrystals_dilithium2_SECRETKEYBYTES
#define pqcrystals_dilithium2_ref_BYTES pqcrystals_dilithium2_BYTES

#ifdef BORINGSSL_PREFIX
#define pqcrystals_dilithium2_ref_keypair BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2_ref_keypair)
#define pqcrystals_dilithium2_ref_signature BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2_ref_signature)
#define pqcrystals_dilithium2_ref BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2_ref)
#define pqcrystals_dilithium2_ref_verify BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2_ref_verify)
#define pqcrystals_dilithium2_ref_open BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2_ref_open)
#endif

int pqcrystals_dilithium2_ref_keypair(uint8_t *pk, uint8_t *sk);

int pqcrystals_dilithium2_ref_signature(uint8_t *sig, size_t *siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *sk);

int pqcrystals_dilithium2_ref(uint8_t *sm, size_t *smlen,
                              const uint8_t *m, size_t mlen,
                              const uint8_t *sk);

int pqcrystals_dilithium2_ref_verify(const uint8_t *sig, size_t siglen,
                                     const uint8_t *m, size_t mlen,
                                     const uint8_t *pk);

int pqcrystals_dilithium2_ref_open(uint8_t *m, size_t *mlen,
                                   const uint8_t *sm, size_t smlen,
                                   const uint8_t *pk);

#define pqcrystals_dilithium2aes_ref_PUBLICKEYBYTES pqcrystals_dilithium2_ref_PUBLICKEYBYTES
#define pqcrystals_dilithium2aes_ref_SECRETKEYBYTES pqcrystals_dilithium2_ref_SECRETKEYBYTES
#define pqcrystals_dilithium2aes_ref_BYTES pqcrystals_dilithium2_ref_BYTES

#ifdef BORINGSSL_PREFIX
#define pqcrystals_dilithium2aes_ref_keypair BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2aes_ref_keypair)
#define pqcrystals_dilithium2aes_ref_signature BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2aes_ref_signature)
#define pqcrystals_dilithium2aes_ref BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2aes_ref)
#define pqcrystals_dilithium2aes_ref_verify BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2aes_ref_verify)
#define pqcrystals_dilithium2aes_ref_open BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium2aes_ref_open)
#endif

int pqcrystals_dilithium2aes_ref_keypair(uint8_t *pk, uint8_t *sk);

int pqcrystals_dilithium2aes_ref_signature(uint8_t *sig, size_t *siglen,
                                           const uint8_t *m, size_t mlen,
                                           const uint8_t *sk);

int pqcrystals_dilithium2aes_ref(uint8_t *sm, size_t *smlen,
                                 const uint8_t *m, size_t mlen,
                                 const uint8_t *sk);

int pqcrystals_dilithium2aes_ref_verify(const uint8_t *sig, size_t siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *pk);

int pqcrystals_dilithium2aes_ref_open(uint8_t *m, size_t *mlen,
                                      const uint8_t *sm, size_t smlen,
                                      const uint8_t *pk);

#define pqcrystals_dilithium3_PUBLICKEYBYTES 1952
#define pqcrystals_dilithium3_SECRETKEYBYTES 4000
#define pqcrystals_dilithium3_BYTES 3293

#define pqcrystals_dilithium3_ref_PUBLICKEYBYTES pqcrystals_dilithium3_PUBLICKEYBYTES
#define pqcrystals_dilithium3_ref_SECRETKEYBYTES pqcrystals_dilithium3_SECRETKEYBYTES
#define pqcrystals_dilithium3_ref_BYTES pqcrystals_dilithium3_BYTES

#ifdef BORINGSSL_PREFIX
#define pqcrystals_dilithium3_ref_keypair BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3_ref_keypair)
#define pqcrystals_dilithium3_ref_signature BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3_ref_signature)
#define pqcrystals_dilithium3_ref BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3_ref)
#define pqcrystals_dilithium3_ref_verify BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3_ref_verify)
#define pqcrystals_dilithium3_ref_open BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3_ref_open)
#endif

int pqcrystals_dilithium3_ref_keypair(uint8_t *pk, uint8_t *sk);

int pqcrystals_dilithium3_ref_signature(uint8_t *sig, size_t *siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *sk);

int pqcrystals_dilithium3_ref(uint8_t *sm, size_t *smlen,
                              const uint8_t *m, size_t mlen,
                              const uint8_t *sk);

int pqcrystals_dilithium3_ref_verify(const uint8_t *sig, size_t siglen,
                                     const uint8_t *m, size_t mlen,
                                     const uint8_t *pk);

int pqcrystals_dilithium3_ref_open(uint8_t *m, size_t *mlen,
                                   const uint8_t *sm, size_t smlen,
                                   const uint8_t *pk);

#define pqcrystals_dilithium3aes_ref_PUBLICKEYBYTES pqcrystals_dilithium3_ref_PUBLICKEYBYTES
#define pqcrystals_dilithium3aes_ref_SECRETKEYBYTES pqcrystals_dilithium3_ref_SECRETKEYBYTES
#define pqcrystals_dilithium3aes_ref_BYTES pqcrystals_dilithium3_ref_BYTES

#ifdef BORINGSSL_PREFIX
#define pqcrystals_dilithium3aes_ref_keypair BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3aes_ref_keypair)
#define pqcrystals_dilithium3aes_ref_signature BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3aes_ref_signature)
#define pqcrystals_dilithium3aes_ref BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3aes_ref)
#define pqcrystals_dilithium3aes_ref_verify BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3aes_ref_verify)
#define pqcrystals_dilithium3aes_ref_open BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium3aes_ref_open)
#endif


int pqcrystals_dilithium3aes_ref_keypair(uint8_t *pk, uint8_t *sk);

int pqcrystals_dilithium3aes_ref_signature(uint8_t *sig, size_t *siglen,
                                           const uint8_t *m, size_t mlen,
                                           const uint8_t *sk);

int pqcrystals_dilithium3aes_ref(uint8_t *sm, size_t *smlen,
                                 const uint8_t *m, size_t mlen,
                                 const uint8_t *sk);

int pqcrystals_dilithium3aes_ref_verify(const uint8_t *sig, size_t siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *pk);

int pqcrystals_dilithium3aes_ref_open(uint8_t *m, size_t *mlen,
                                      const uint8_t *sm, size_t smlen,
                                      const uint8_t *pk);

#define pqcrystals_dilithium5_PUBLICKEYBYTES 2592
#define pqcrystals_dilithium5_SECRETKEYBYTES 4864
#define pqcrystals_dilithium5_BYTES 4595

#define pqcrystals_dilithium5_ref_PUBLICKEYBYTES pqcrystals_dilithium5_PUBLICKEYBYTES
#define pqcrystals_dilithium5_ref_SECRETKEYBYTES pqcrystals_dilithium5_SECRETKEYBYTES
#define pqcrystals_dilithium5_ref_BYTES pqcrystals_dilithium5_BYTES

#ifdef BORINGSSL_PREFIX
#define pqcrystals_dilithium5_ref_keypair BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5_ref_keypair)
#define pqcrystals_dilithium5_ref_signature BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5_ref_signature)
#define pqcrystals_dilithium5_ref BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5_ref)
#define pqcrystals_dilithium5_ref_verify BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5_ref_verify)
#define pqcrystals_dilithium5_ref_open BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5_ref_open)
#endif

int pqcrystals_dilithium5_ref_keypair(uint8_t *pk, uint8_t *sk);

int pqcrystals_dilithium5_ref_signature(uint8_t *sig, size_t *siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *sk);

int pqcrystals_dilithium5_ref(uint8_t *sm, size_t *smlen,
                              const uint8_t *m, size_t mlen,
                              const uint8_t *sk);

int pqcrystals_dilithium5_ref_verify(const uint8_t *sig, size_t siglen,
                                     const uint8_t *m, size_t mlen,
                                     const uint8_t *pk);

int pqcrystals_dilithium5_ref_open(uint8_t *m, size_t *mlen,
                                   const uint8_t *sm, size_t smlen,
                                   const uint8_t *pk);

#define pqcrystals_dilithium5aes_ref_PUBLICKEYBYTES pqcrystals_dilithium5_ref_PUBLICKEYBYTES
#define pqcrystals_dilithium5aes_ref_SECRETKEYBYTES pqcrystals_dilithium5_ref_SECRETKEYBYTES
#define pqcrystals_dilithium5aes_ref_BYTES pqcrystals_dilithium5_ref_BYTES

#ifdef BORINGSSL_PREFIX
#define pqcrystals_dilithium5aes_ref_keypair BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5aes_ref_keypair)
#define pqcrystals_dilithium5aes_ref_signature BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5aes_ref_signature)
#define pqcrystals_dilithium5aes_ref BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5aes_ref)
#define pqcrystals_dilithium5aes_ref_verify BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5aes_ref_verify)
#define pqcrystals_dilithium5aes_ref_open BORINGSSL_ADD_PREFIX(BORINGSSL_PREFIX, pqcrystals_dilithium5aes_ref_open)
#endif


int pqcrystals_dilithium5aes_ref_keypair(uint8_t *pk, uint8_t *sk);

int pqcrystals_dilithium5aes_ref_signature(uint8_t *sig, size_t *siglen,
                                           const uint8_t *m, size_t mlen,
                                           const uint8_t *sk);

int pqcrystals_dilithium5aes_ref(uint8_t *sm, size_t *smlen,
                                 const uint8_t *m, size_t mlen,
                                 const uint8_t *sk);

int pqcrystals_dilithium5aes_ref_verify(const uint8_t *sig, size_t siglen,
                                        const uint8_t *m, size_t mlen,
                                        const uint8_t *pk);

int pqcrystals_dilithium5aes_ref_open(uint8_t *m, size_t *mlen,
                                      const uint8_t *sm, size_t smlen,
                                      const uint8_t *pk);


#endif
