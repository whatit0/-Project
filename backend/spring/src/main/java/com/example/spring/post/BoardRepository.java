package com.example.spring.post;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface BoardRepository extends JpaRepository<BoardEntity, Integer> {

    // 조회수 증가
    @Modifying
    @Query(value = "update BoardEntity b set b.postcnt = b.postcnt + 1 where b.postno = :postno")
    void updateHit(@Param("postno") int postno);
}
